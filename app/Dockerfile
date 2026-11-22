# Start from a small official Python image
FROM python:3.12-slim

# Python settings suited to containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# All following commands run in /app inside the image
WORKDIR /app

# Create a non-root user to run the app
RUN useradd --create-home appuser

# Install dependencies first (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the application code
COPY app.py .

# Drop root privileges
USER appuser

# Document which port the app listens on
EXPOSE 5000

# Let Docker check the app is healthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Start the app with gunicorn (production web server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
