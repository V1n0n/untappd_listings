# Stage 1: Define the base image
FROM python AS base

# Non-root user for security compliance
RUN useradd --create-home appuser && chown -R appuser:appuser /home/appuser
WORKDIR /home/appuser
USER appuser

# Stage 3: Copy dependency files (if any)
COPY requirements.txt .

# Stage 4: Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4.1: Install elements (if any)
RUN python -m playwright install chromium

# Stage 5: Copy the application script
COPY src/untappd_csv_additions.py .