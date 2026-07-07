In Python is de belangrijkste naamgevingsrichtlijn: **volg PEP 8**. Hieronder de meest gebruikte best practices.

## Algemene principes

- Gebruik **duidelijke, beschrijvende namen**.
- Vermijd afkortingen tenzij ze algemeen bekend zijn.
- Kies namen die uitleggen **wat iets is of doet**.
- Wees consistent binnen je project.
- Gebruik Engels als je project internationaal of professioneel gedeeld wordt.
- Gebruik Nederlands alleen als het hele project/domein bewust Nederlandstalig is.

## Variabelen en functies

Gebruik **snake_case**:

```python
user_name = "Alice"
total_price = 42.50
is_active = True
```


Functies ook in **snake_case**:

```python
def calculate_total_price(items):
    ...
```


Goede functienamen zijn meestal werkwoorden of werkwoordzinnen:

```python
def load_users():
    ...

def validate_email_address(email):
    ...

def send_invoice(invoice):
    ...
```


## Classes

Gebruik **PascalCase**:

```python
class UserAccount:
    ...

class InvoiceProcessor:
    ...
```


Classnamen zijn meestal zelfstandige naamwoorden.

## Constanten

Gebruik **UPPER_SNAKE_CASE**:

```python
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://example.com"
```


Let op: Python dwingt constanten niet af, maar deze stijl geeft aan: “niet wijzigen”.

## Modules en bestanden

Gebruik korte namen in **snake_case**:

```plain text
user_service.py
invoice_processor.py
data_loader.py
```


Vermijd hoofdletters, spaties en streepjes in bestandsnamen:

```plain text
# Liever niet
UserService.py
invoice-processor.py
data loader.py
```


## Packages

Packages zijn meestal kort en lowercase:

```plain text
users/
billing/
reports/
```


Bij voorkeur zonder underscores, tenzij het de leesbaarheid sterk verbetert.

## Private of interne namen

Gebruik een enkele underscore voor interne functies, variabelen of methodes:

```python
def _parse_internal_config():
    ...
```


Bij classes:

```python
class UserService:
    def _build_payload(self):
        ...
```


Dit betekent conventioneel: “bedoeld voor intern gebruik”.

## Vermijd dubbele underscores tenzij nodig

Dubbele underscores activeren name mangling:

```python
class Example:
    def __internal_method(self):
        ...
```


Gebruik dit zelden. Meestal is één underscore genoeg.

## Speciale magic methods

Dubbele underscores aan beide kanten zijn gereserveerd voor Python zelf:

```python
def __init__(self):
    ...

def __str__(self):
    ...
```


Maak zelf geen willekeurige namen zoals:

```python
def __do_something__():
    ...
```


## Booleans

Boolean variabelen klinken vaak goed met `is_`, `has_`, `can_` of `should_`:

```python
is_valid = True
has_permission = False
can_retry = True
should_send_email = False
```


Vermijd vage namen:

```python
# Minder duidelijk
flag = True
status = False
```


## Collecties

Gebruik meervoud voor lijsten, sets en andere collecties:

```python
users = []
email_addresses = set()
orders_by_id = {}
```


Voor dictionaries kan een naam als `x_by_y` duidelijk zijn:

```python
users_by_id = {
    1: "Alice",
    2: "Bob",
}
```


## Afkortingen en acroniemen

Wees consistent. In Python zie je vaak:

```python
api_url = "..."
html_parser = "..."
user_id = 123
```


Bij classes:

```python
class ApiClient:
    ...

class HtmlParser:
    ...
```


Sommige teams gebruiken `APIClient`, maar `ApiClient` past vaak beter bij normale PascalCase-consistentie.

## Namen die je beter vermijdt

Vermijd namen die Python built-ins overschrijven:

```python
# Niet doen
list = [1, 2, 3]
dict = {"a": 1}
str = "hello"
id = 123
file = open("data.txt")
```


Gebruik liever:

```python
numbers = [1, 2, 3]
user_by_name = {"a": 1}
text = "hello"
user_id = 123
input_file = open("data.txt")
```


## Loopvariabelen

Korte namen mogen als de context heel duidelijk is:

```python
for user in users:
    print(user.name)
```


Voor indexen is dit prima:

```python
for i, item in enumerate(items):
    ...
```


Maar vermijd onduidelijke namen in complexere code:

```python
# Minder goed
for x in data:
    ...
```


## Type aliases en type variables

Type aliases meestal in PascalCase:

```python
UserId = int
JsonDict = dict[str, object]
```


Type variables vaak kort en in PascalCase:

```python
from typing import TypeVar

T = TypeVar("T")
UserT = TypeVar("UserT")
```


## Exceptions

Custom exceptions eindigen meestal op `Error`:

```python
class ValidationError(Exception):
    ...

class PaymentFailedError(Exception):
    ...
```


## Voorbeelden: slecht versus beter

```python
# Minder goed
def calc(x, y):
    return x * y
```


```python
# Beter
def calculate_total_price(quantity, unit_price):
    return quantity * unit_price
```


```python
# Minder goed
d = {"alice": 1}
```


```python
# Beter
user_ids_by_name = {"alice": 1}
```


## Samenvatting

| Element | Stijl | Voorbeeld |
|---|---|---|
| Variabele | `snake_case` | `user_name` |
| Functie | `snake_case` | `calculate_total` |
| Methode | `snake_case` | `send_email` |
| Class | `PascalCase` | `UserAccount` |
| Constante | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Module/bestand | `snake_case.py` | `data_loader.py` |
| Package | lowercase | `billing` |
| Intern/private | `_leading_underscore` | `_parse_config` |
| Exception | `PascalCase` + `Error` | `ValidationError` |

Kort gezegd: **gebruik `snake_case` voor bijna alles, `PascalCase` voor classes en `UPPER_SNAKE_CASE` voor constanten**.