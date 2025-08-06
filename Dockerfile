FROM python:3.9-slim

# wkhtmltopdf quraşdır
RUN apt-get update && apt-get install -y wkhtmltopdf

# İşçi qovluğu təyin et
WORKDIR /app

# Layihə fayllarını köçür
COPY . .

# Asılılıqları quraşdır
RUN pip install -r requirements.txt

# Gunicorn ilə tətbiqi işə sal
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
