from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router

# Veritabanı tablolarını oluştur (Basit projeler için ideal, gelişmiş sistemlerde Alembic kullanılır)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gelişmiş URL Shortener API",
    description="Ölçeklenebilir, Redis önbellekleme destekli URL kısaltma servisi.",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def read_root():
    return {
        "message": "URL Shortener servisi çalışıyor!",
        "docs": "Swagger UI için `/docs` adresine gidebilirsiniz."
    }
