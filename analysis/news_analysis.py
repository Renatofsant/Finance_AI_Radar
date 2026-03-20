import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = st.secrets.get("NEWS_API_KEY") or os.getenv("NEWS_API_KEY")


def buscar_noticias(ativo):

    nome = ativo.split(".")[0]

    # 🔥 MAPEAMENTO INTELIGENTE
    mapa = {
        "PETR4": "Petrobras",
        "VALE3": "Vale mineração",
        "ITUB4": "Itaú banco",
        "BBDC4": "Bradesco banco",
        "ABEV3": "Ambev",
        "WEGE3": "Weg indústria",
        "MGLU3": "Magazine Luiza",
        "BBAS3": "Banco do Brasil",
        "LREN3": "Lojas Renner",
        "SUZB3": "Suzano papel celulose"
    }

    query = mapa.get(nome, nome)

    url = f"https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=publishedAt&pageSize=5&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    noticias = []

    for artigo in data.get("articles", []):
        noticias.append({
            "titulo": artigo.get("title"),
            "descricao": artigo.get("description")
        })

    return noticias
