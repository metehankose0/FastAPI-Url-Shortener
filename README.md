# 🚀 Gelişmiş URL Shortener API (Redis + PostgreSQL + Docker)

Bu proje, yüksek performanslı ve ölçeklenebilir bir mimariye sahip, modern bir **URL Kısaltma (URL Shortener) Mikroservisidir**. FastAPI ile geliştirilmiş olup, arka planda veri kalıcılığı için **PostgreSQL**, yanıt sürelerini milisaniyelere düşüren önbellekleme (caching) mekanizması için ise **Redis** kullanmaktadır.

Sistemin kurulumunu ve taşınabilirliğini sıfır efora indirmek için **Docker & Docker Compose** ile tamamen containerize edilmiştir.

## ✨ Neden Bu Mimari? (Sistem Tasarımı Özeti)

URL kısaltma sistemleri ("read-heavy" yani okuma ağırlıklı sistemlerdir) genellikle çok fazla yönlendirme isteği alırlar ancak yeni link ekleme istekleri buna kıyasla azdır. Bu problemin üstesinden gelmek için projede aşağıdaki yapı tercih edilmiştir:

1.  **FastAPI (Backend):** Asenkron destekli, hızlı ve Swagger UI ile kendiliğinden belgelenen modern bir Python framework'ü.
2.  **PostgreSQL (Veritabanı):** Kısaltılmış kodların, uzun URL karşılıklarının ve tıklanma istatistiklerinin (analytics) güvenle kalıcı olarak saklandığı veritabanı.
3.  **Redis (Cache Katmanı):** Sistemin darboğaz (bottleneck) yaşamasını engelleyen en büyük faktördür. Okuma hızı saniyenin altındadır. Eğer kullanıcı daha önce tıklanıp Cache'e alınan bir kısa URL'e istek yaparsa, sistem **PostgreSQL veritabanını hiç yormadan** (sorgu atmadan) doğrudan RAM (Redis) üzerinden saniyeden çok daha kısa bir sürede yönlendirme yapar.
4.  **Docker Compose:** Bağımlılık problemlerini (It works on my machine problemini) yok etmek için tüm altyapı Docker ile tek komutta ayağa kalkar.

---

## 🛠️ Kullanılan Teknolojiler

- **Dil/Framework:** Python 3.11, FastAPI, Pydantic, SQLAlchemy
- **Database:** PostgreSQL (v15)
- **Cache:** Redis (v7)
- **DevOps:** Docker, Docker Compose, Uvicorn

---

## 📥 Kurulum ve Çalıştırma

Bilgisayarınızda **Docker** ve **Docker Compose** kurulu olması yeterlidir. Önceden hiçbir Python, Postgres veya Redis eklentisi kurmanıza gerek yoktur.

1. Projeyi bilgisayarınıza indirin (veya klonlayın) ve proje dizinine gidin:
```bash
cd url_shortener
```

2. Docker Compose ile tüm mimariyi (Database, Cache, API) arka planda ayağa kaldırın:
```bash
docker-compose up -d --build
```

3. Kurulum tamamlandıktan sonra uygulama şurada çalışıyor olacaktır:
   - **API Test Paneli (Swagger UI):** 👉 [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Ana Sayfa:** 👉 [http://localhost:8000/](http://localhost:8000/)

---

## 🎯 API Endpoint'leri (Kullanım)

Uygulama çalıştıktan sonra `http://localhost:8000/docs` adresinden tüm endpoint'leri arayüz üzerinden test edebilirsiniz. Veya herhangi bir aracı (Postman, cURL) kullanabilirsiniz.

### 1. Yeni URL Kısaltma `POST /shorten`
Uzun URL'yi vererek sistemden rastgele benzersiz bir kısa kod (`short_code`) alırsınız.
**İstek (Request Body):**
```json
{
  "original_url": "https://www.google.com/search?q=sistem+tasarimi+nasil+ogrenilir"
}
```
**Yanıt (Response Body):**
```json
{
  "original_url": "https://www.google.com/search?q=sistem+tasarimi+nasil+ogrenilir",
  "short_code": "xYz123",
  "clicks": 0,
  "created_at": "2024-10-25T14:32:00Z"
}
```

### 2. Kısa URL Yönlendirmesi `GET /{short_code}`
Oluşturulan kısa linke tarayıcıdan gidildiğinde çalışır. (Örn: `http://localhost:8000/xYz123`)
* **Nasıl Çalışır?:** Önce Cache (Redis) kontrol edilir. Varsa direkt, yoksa veritabanından alınıp Cache'e eklenir (`TTL: 1 Saat`). Tıklanma sayısı arkaplanda güncellenir.

### 3. İstatistik Görüntüleme `GET /v1/stats/{short_code}`
Belirli bir linkin analiz/analitik detaylarını döner. (Sistemi test edip tıklanmaların `clicks` değişkeninde artıp artmadığını görebilirsiniz).

---

## 🧹 Sistemi Kapatma

Çalışan tüm docker container'larını durdurmak ve temizlemek isterseniz bu komutu kullanın:
```bash
docker-compose down
```
*(Not: Volume tanımlamaları yapıldığı için verileriniz `docker-compose down` sonrası silinmez. Ancak temiz başlamak isterseniz `docker-compose down -v` komutunu kullanabilirsiniz.)*
