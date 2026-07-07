#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from rapidfuzz import fuzz

import general_functions

BASE_URL = "https://untappd.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,nl;q=0.8",
}

@dataclass
class UntappdResult:
    rating: str
    rating_count: str
    url: str
    confidence: int

def _get_soup(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def _find_candidate_urls_with_browser(search_url: str) -> list[str]:
    urls: list[str] = []

    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=HEADERS["User-Agent"]
        )

        page.goto(search_url, wait_until="networkidle", timeout=30000)

        links = page.locator("a[href^='/beer/']").evaluate_all(
            """els => els.map(a => a.getAttribute('href'))"""
        )

        browser.close()

    for href in links:
        if not href:
            continue

        full = urljoin(BASE_URL, href.split("?")[0])
        if full not in urls:
            urls.append(full)

        if len(urls) >= 8:
            break

    return urls

def _find_candidate_urls(brewery: str, beer: str) -> list[str]:
    query = quote_plus(f'{brewery}, {beer}')
    search_url = f"{BASE_URL}/search?q={query}&type=beer&sort=brewery"

    return _find_candidate_urls_with_browser(search_url)

def _extract_title(soup: BeautifulSoup) -> str:
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return  og_title.get("content")
    if soup.title and soup.title.string:
        return soup.title.string
    h1 = soup.find("h1")
    return h1.get_text(" ", strip=True) if h1 else ""

def _extract_count(soup: BeautifulSoup) -> Optional[int]:
    text = soup.get_text(" ", strip=True)

    count: Optional[int] = None

    count_patterns = [
        r"([\d,\.]+\s*[kKmM]?)\s+Ratings\b",
        r"Ratings\s*[:\-]?\s*([\d,\.]+\s*[kKmM]?)",
    ]
    for pattern in count_patterns:
        m = re.search(pattern, text, re.I)
        if m:
            count = general_functions.parse_number(m.group(1))
            if count is not None:
                break

    return count


def _extract_rating(soup: BeautifulSoup) -> Optional[str]:
    text = soup.get_text(" ", strip=True)

    rating: Optional[str] = None
    rating_patterns = [
        r"(?:Global\s+)?Rating\s*[:\-]?\s*(\d\.\d{1,3})",
        r"(\d\.\d{1,3})\s*(?:/\s*5)?\s*(?:Global\s+)?Rating",
    ]
    for pattern in rating_patterns:
        m = re.search(pattern, text, re.I)
        if m:
            rating = m.group(1)
            break

    return rating


def lookup_untappd(session: requests.Session, brewery: str, beer: str) -> Optional[UntappdResult]:
    expected = general_functions.normalize(f"{beer} {brewery}")
    urls = _find_candidate_urls(brewery, beer)

    best: Optional[UntappdResult] = None
    for url in urls:
        try:
            soup = _get_soup(session, url)
        except Exception:
            continue

        title = general_functions.normalize(_extract_title(soup))
        confidence = fuzz.token_set_ratio(expected, title)

        rating = _extract_rating(soup)
        count = _extract_count(soup)

        if rating is None or count is None:
            continue

        result = UntappdResult(
            rating=rating,
            rating_count=str(count),
            url=url,
            confidence=int(confidence),
        )
        if best is None or result.confidence > best.confidence:
            best = result

    if best and best.confidence >= 78:
        return best
    return None
