FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main_scraper.py .

RUN mkdir -p /tmp/scraper/output && \
    chmod -R 777 /tmp/scraper

CMD ["python", "main_scraper.py"]