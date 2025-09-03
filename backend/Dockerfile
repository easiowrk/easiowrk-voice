FROM python:3.11-slim

WORKDIR /app

# Install OS dependencies for building wheels and connecting via SSL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Upgrade pip & install with longer timeout
RUN pip install --upgrade pip setuptools wheel \
 && pip install --default-timeout=200 --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose API port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
