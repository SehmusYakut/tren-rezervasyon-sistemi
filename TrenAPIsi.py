from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

class Vagon(BaseModel):
    Ad: str
    Kapasite: int
    DoluKoltukAdet: int

class Tren(BaseModel):
    Ad: str
    Vagonlar: List[Vagon]

class RezervasyonInput(BaseModel):
    Tren: Tren
    RezervasyonYapilacakKisiSayisi: int
    KisilerFarkliVagonlaraYerlestirilebilir: bool

class YerlesimAyrinti(BaseModel):
    VagonAdi: str
    KisiSayisi: int

class RezervasyonOutput(BaseModel):
    RezervasyonYapilabilir: bool
    YerlesimAyrinti: List[YerlesimAyrinti]

@app.post("/rezervasyon", response_model=RezervasyonOutput)
async def rezervasyon_yap(input_data: RezervasyonInput):
    tren = input_data.Tren
    kisi_sayisi = input_data.RezervasyonYapilacakKisiSayisi
    farkli_vagon = input_data.KisilerFarkliVagonlaraYerlestirilebilir
    
    # Vagonları boş koltuk sayısına göre sırala (azalan)
    vagonlar = sorted(tren.Vagonlar, key=lambda v: v.Kapasite - v.DoluKoltukAdet, reverse=True)
    
    yerlesim = []
    
    if not farkli_vagon:
        # Aynı vagona yerleştir
        for vagon in vagonlar:
            bos_koltuk = vagon.Kapasite - vagon.DoluKoltukAdet
            if bos_koltuk >= kisi_sayisi:
                # Rezervasyon sonrası doluluk kontrolü
                yeni_dolu = vagon.DoluKoltukAdet + kisi_sayisi
                yeni_doluluk = yeni_dolu / vagon.Kapasite
                if yeni_doluluk <= 0.7:
                    yerlesim.append(YerlesimAyrinti(VagonAdi=vagon.Ad, KisiSayisi=kisi_sayisi))
                    return RezervasyonOutput(RezervasyonYapilabilir=True, YerlesimAyrinti=yerlesim)
        # Uygun vagon bulunamadı
        return RezervasyonOutput(RezervasyonYapilabilir=False, YerlesimAyrinti=[])
    else:
        # Farklı vagonlara dağıt
        kalan_kisi = kisi_sayisi
        for vagon in vagonlar:
            if kalan_kisi <= 0:
                break
            bos_koltuk = vagon.Kapasite - vagon.DoluKoltukAdet
            if bos_koltuk > 0:
                # Maksimum yerleştirilebilir kişi sayısı (rezervasyon sonrası %70'i geçmemeli)
                max_yerlestirilebilir = int((vagon.Kapasite * 0.7) - vagon.DoluKoltukAdet)
                yerlestirilecek = min(bos_koltuk, kalan_kisi, max(max_yerlestirilebilir, 0))
                if yerlestirilecek > 0:
                    yerlesim.append(YerlesimAyrinti(VagonAdi=vagon.Ad, KisiSayisi=yerlestirilecek))
                    kalan_kisi -= yerlestirilecek
        
        if kalan_kisi > 0:
            # Tüm kişileri yerleştiremedik
            return RezervasyonOutput(RezervasyonYapilabilir=False, YerlesimAyrinti=[])
        
        return RezervasyonOutput(RezervasyonYapilabilir=True, YerlesimAyrinti=yerlesim)

@app.get("/")
async def root():
    return {"message": "Tren Rezervasyon API'si"}

