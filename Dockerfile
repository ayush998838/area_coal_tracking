# Streamlit container for Cloud Run
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /app

# System deps needed by pdfplumber/tabula
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    build-essential \
    ghostscript \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run app.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --browser.gatherUsageStats=false \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
