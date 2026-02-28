# Resmi hafif Python imajı
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli sistem kütüphanelerini kur (PostgreSQL driver'ı için psycopg2-binary'e yardımcı)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamanın tamamını kopyala
COPY ./app ./app

# API isteğini kabul edecek port numarası
EXPOSE 8000

# Container başlatıldığında çalıştırılacak komut
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
