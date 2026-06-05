# Python imajını kullan (RPi5 ARM mimarisiyle uyumludur)
FROM python:3.11-slim

# Çevresel değişkenler
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Gereksinimler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Entrypoint script'i çalıştırılabilir yap
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Port
EXPOSE 8000

# Entrypoint: collectstatic + migrate + gunicorn
ENTRYPOINT ["sh", "./entrypoint.sh"]
