import requests

TOKEN = "8212900138:AAHKpjUWwur_FKLpdumWkZ2SL_xRxtw52Fw"
CHAT_ID = "1831733779"

def enviar_alerta(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })