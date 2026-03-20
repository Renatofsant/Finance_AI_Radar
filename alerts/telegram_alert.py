import requests
import streamlit as st

# Puxa os dados das Secrets do Streamlit Cloud
TOKEN = st.secrets.get("TELEGRAM_TOKEN")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID")

def enviar_alerta(msg):
    if not TOKEN or not CHAT_ID:
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")
