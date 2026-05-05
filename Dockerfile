# Use stable Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]