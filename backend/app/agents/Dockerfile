FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code (including agents worker)
COPY backend .

# Default command: run the LiveKit agent worker
CMD ["python", "-m", "app.agents.agents_worker", "start"]
