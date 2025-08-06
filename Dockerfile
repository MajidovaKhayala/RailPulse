FROM python:3.9-slim

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
