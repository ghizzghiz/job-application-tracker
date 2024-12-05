FROM python:3.9-slim

# System dependencies for PostgreSQL and netcat
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application code into the container
COPY . .
COPY .env /app/.env

# Set the entrypoint script to run
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose the FastAPI port
EXPOSE 8000