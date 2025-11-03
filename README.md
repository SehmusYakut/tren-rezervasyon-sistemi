# Tren Rezervasyon Sistemi

Bu proje, tren rezervasyonları için modern bir web uygulamasıdır. Streamlit tabanlı kullanıcı arayüzü ve FastAPI tabanlı backend API'sinden oluşur.

## Özellikler

- **Akıllı Rezervasyon**: Kişileri vagonlara yerleştirirken %70 doluluk kuralını uygular
- **Esnek Yerleştirme**: Aynı vagona veya farklı vagonlara yerleştirme seçeneği
- **Modern UI**: Streamlit ile kullanıcı dostu arayüz
- **REST API**: FastAPI ile güçlü backend

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install streamlit fastapi uvicorn requests pandas
```

2. API'yi çalıştırın:
```bash
uvicorn TrenAPIsi:app --reload
```

3. UI'yi çalıştırın:
```bash
streamlit run app.py
```

## Kullanım

1. **API'yi başlatın**: `http://localhost:8000`
2. **UI'yi açın**: `http://localhost:8501`
3. **Rezervasyon yapın**: Tren seçin, kişi sayısı belirleyin, yerleştirme tercihini seçin

## API Dokümantasyonu

API dokümantasyonuna `http://localhost:8000/docs` adresinden ulaşabilirsiniz.

### Rezervasyon Endpoint'i

**POST /rezervasyon**

Input formatı:
```json
{
    "Tren": {
        "Ad": "Başkent Ekspres",
        "Vagonlar": [
            {"Ad": "Vagon 1", "Kapasite": 100, "DoluKoltukAdet": 65}
        ]
    },
    "RezervasyonYapilacakKisiSayisi": 3,
    "KisilerFarkliVagonlaraYerlestirilebilir": true
}
```

Output formatı:
```json
{
    "RezervasyonYapilabilir": true,
    "YerlesimAyrinti": [
        {"VagonAdi": "Vagon 1", "KisiSayisi": 3}
    ]
}
```

## Kurallar

- Bir vagonun doluluk oranı rezervasyon sonrası %70'i geçemez
- Sistem "ya hepsi ya hiç" mantığıyla çalışır
- Kısmi yerleştirme yapılmaz

## Teknoloji Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Language**: Python 3.8+
- **Data Validation**: Pydantic