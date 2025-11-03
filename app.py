import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Sayfa başlığı
st.title("🚂 Tren Rezervasyon Sistemi")

# Sidebar ile navigasyon yerine tabs kullan
tab1, tab2, tab3 = st.tabs(["🏠 Ana Sayfa", "🎫 Rezervasyon Yap", "📋 Rezervasyonlarım"])

with tab1:
    st.header("Hoş Geldiniz!")
    st.write("Tren rezervasyonunuzu kolayca yapın.")
    
    # Arama formu
    st.subheader("Tren Ara")
    col1, col2 = st.columns(2)
    
    with col1:
        kalkis = st.text_input("Kalkış İstasyonu", placeholder="İstanbul")
        tarih = st.date_input("Tarih", min_value=datetime.today())
    
    with col2:
        varis = st.text_input("Varış İstasyonu", placeholder="Ankara")
        yolcu_sayisi = st.number_input("Yolcu Sayısı", min_value=1, max_value=10, value=1)
    
    if st.button("Ara"):
        st.success("Arama yapıldı!")
        
        # Mock tren verileri
        trenler = pd.DataFrame({
            "Tren No": ["T001", "T002", "T003"],
            "Kalkış": ["İstanbul", "İstanbul", "İstanbul"],
            "Varış": ["Ankara", "Ankara", "Ankara"],
            "Saat": ["08:00", "12:00", "16:00"],
            "Süre": ["4 saat", "4 saat", "4 saat"],
            "Fiyat": ["₺150", "₺160", "₺155"]
        })
        
        st.subheader("Müsait Trenler")
        selected_tren = st.selectbox("Tren Seçin", trenler["Tren No"])
        
        if selected_tren:
            tren_detay = trenler[trenler["Tren No"] == selected_tren].iloc[0]
            st.write(f"Seçilen Tren: {tren_detay['Tren No']} - {tren_detay['Kalkış']} → {tren_detay['Varış']}")
            st.write(f"Saat: {tren_detay['Saat']}, Süre: {tren_detay['Süre']}, Fiyat: {tren_detay['Fiyat']}")
            
            if st.button("Rezervasyon Yap"):
                st.session_state["selected_tren"] = tren_detay
                st.success("Rezervasyon sayfasına yönlendiriliyorsunuz...")
                st.rerun()

with tab2:
    st.header("Rezervasyon Detayları")
    
    # Tren seçimi
    st.subheader("Tren Seçimi")
    tren_secenekleri = ["Başkent Ekspres", "Ankara Ekspres", "İstanbul Ekspres"]
    selected_tren = st.selectbox("Tren Seçin", tren_secenekleri)
    
    # Rezervasyon bilgileri
    st.subheader("Rezervasyon Bilgileri")
    col1, col2 = st.columns(2)
    
    with col1:
        kisi_sayisi = st.number_input("Rezervasyon Yapılacak Kişi Sayısı", min_value=1, max_value=10, value=1)
    
    with col2:
        farkli_vagon = st.checkbox("Kişiler Farklı Vagonlara Yerleştirilebilir", value=False)
    
    # Yolcu bilgileri formu
    st.subheader("Yolcu Bilgileri")
    yolcular = []
    for i in range(kisi_sayisi):
        st.write(f"**Yolcu {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            ad = st.text_input(f"Ad {i+1}", key=f"ad_{i}")
            soyad = st.text_input(f"Soyad {i+1}", key=f"soyad_{i}")
        with col2:
            tc = st.text_input(f"TC Kimlik No {i+1}", key=f"tc_{i}")
            email = st.text_input(f"E-posta {i+1}", key=f"email_{i}")
        telefon = st.text_input(f"Telefon {i+1}", key=f"telefon_{i}")
        yolcular.append({
            "ad": ad,
            "soyad": soyad,
            "tc": tc,
            "email": email,
            "telefon": telefon
        })
    
    if st.button("Rezervasyon Yap"):
        # Input JSON oluştur
        input_json = {
            "Tren": {
                "Ad": selected_tren,
                "Vagonlar": [
                    {"Ad": "Vagon 1", "Kapasite": 100, "DoluKoltukAdet": 65},
                    {"Ad": "Vagon 2", "Kapasite": 90, "DoluKoltukAdet": 80},
                    {"Ad": "Vagon 3", "Kapasite": 80, "DoluKoltukAdet": 55}
                ]
            },
            "RezervasyonYapilacakKisiSayisi": kisi_sayisi,
            "KisilerFarkliVagonlaraYerlestirilebilir": farkli_vagon
        }
        
        st.subheader("Gönderilen Input JSON")
        st.json(input_json)
        
        # API'ye istek gönder
        try:
            response = requests.post("http://localhost:8000/rezervasyon", json=input_json)
            if response.status_code == 200:
                result = response.json()
                st.subheader("API Dönüş JSON")
                st.json(result)
                
                if result["RezervasyonYapilabilir"]:
                    st.success("Rezervasyon başarıyla yapıldı!")
                    st.balloons()
                else:
                    st.error("Rezervasyon yapılamadı. Yeterli yer bulunamadı.")
            else:
                st.error(f"API hatası: {response.status_code}")
        except Exception as e:
            st.error(f"Bağlantı hatası: {str(e)}")
            # Fallback: placeholder response
            st.subheader("Beklenen Dönüş JSON (Fallback)")
            response_json = {
                "RezervasyonYapilabilir": True,
                "YerlesimAyrinti": [
                    {"VagonAdi": "Vagon 1", "KisiSayisi": 2},
                    {"VagonAdi": "Vagon 2", "KisiSayisi": 1}
                ]
            }
            st.json(response_json)

with tab3:
    st.header("Rezervasyonlarım")
    st.write("Henüz rezervasyonunuz bulunmamaktadır.")