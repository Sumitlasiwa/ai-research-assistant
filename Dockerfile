FROM python:3.12-slim

WORKDIR /code

# Install dependencies first for better build caching.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code.
COPY app/ ./app/

# Create directory for generated reports.
RUN mkdir -p reports

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]