FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Healthcheck & gunicorn example
EXPOSE 8000
CMD ["sh", "-c", "gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
