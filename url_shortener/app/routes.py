from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models, schemas, database, utils

router = APIRouter()

@router.post("/shorten", response_model=schemas.URLInfo)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(database.get_db)):
    # URL veritabanında daha önce kısaltılmış mı kontrol et
    db_url = db.query(models.URL).filter(models.URL.original_url == url.original_url).first()
    if db_url:
        return db_url

    # Benzersiz bir kısa kod üret
    short_code = utils.generate_short_code()
    while db.query(models.URL).filter(models.URL.short_code == short_code).first():
        short_code = utils.generate_short_code()

    # Veritabanına kaydet
    new_url = models.URL(original_url=url.original_url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@router.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(database.get_db)):
    # 1. Önce Redis Cache'e bak
    cached_url = database.redis_client.get(short_code)
    if cached_url:
        # Tıklanma sayısını arkaplanda artırmak (basitlik için direkt artırıyoruz)
        db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if db_url:
            db_url.clicks += 1
            db.commit()
        return RedirectResponse(url=cached_url)

    # 2. Cache'de yoksa Veritabanından getir
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if db_url:
        # Gelecekteki istekler için Redis Cache'i güncelle (1 saat boyunca sakla)
        database.redis_client.setex(short_code, 3600, db_url.original_url)
        
        # Tıklanma sayısını artır
        db_url.clicks += 1
        db.commit()
        
        return RedirectResponse(url=db_url.original_url)

    raise HTTPException(status_code=404, detail="Böyle bir URL bulunamadı.")

@router.get("/v1/stats/{short_code}", response_model=schemas.URLInfo)
def get_url_stats(short_code: str, db: Session = Depends(database.get_db)):
    """URL için kaç defa tıklandığı gibi istatistikleri getirir."""
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if db_url:
        return db_url
    raise HTTPException(status_code=404, detail="URL bulunamadı.")
