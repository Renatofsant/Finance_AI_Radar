import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from scheduler.market_scanner import escanear
from analysis.news_analysis import buscar_noticias
from streamlit_autorefresh import st_autorefresh
from analysis.gpt_analysis import analisar_com_gpt
from analysis.decision_engine import gerar_sinal
from analysis.ultimate_ai import analise_completa
from analysis.sentiment_analysis import analisar_sentimento
from analysis.ai_trader import decisao_trade

# Para rodar, digitar: streamlit run dashboard/dashboard.py no terminal.

# ========================
# CONFIGURAÇÃO DA PÁGINA
# ========================

st.set_page_config(
    page_title="Radar IA Financeiro",
    layout="wide"
)

# ========================
# ESTILO BLOOMBERG
# ========================

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.metric-box {
    padding: 10px;
    border-radius: 10px;
    background-color: #1c1f26;
}

/* 🔥 CURSOR EM TODO O DROPDOWN */
div[data-baseweb="select"] * {
    cursor: pointer !important;
}

/* Hover mais visível */
div[data-baseweb="select"]:hover {
    border: 1px solid #00ffcc;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Radar Inteligente de Mercado (Modo PRO)")

# ========================
# SCANNER (PRIMEIRO)
# ========================

oportunidades = escanear()

# ========================
# SIDEBAR (LISTA INTELIGENTE)
# ========================

st.sidebar.title("⚙️ Configurações")

# LISTA BASE (FIXA)
lista_base = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "ABEV3.SA",
    "WEGE3.SA",
    "MGLU3.SA",
    "BBAS3.SA",
    "LREN3.SA",
    "SUZB3.SA"
]

# JUNTA COM OPORTUNIDADES
if oportunidades:
    ativos_oportunidade = [op["ativo"] for op in oportunidades]
    lista_ativos = list(set(lista_base + ativos_oportunidade))
else:
    lista_ativos = lista_base

# DROPDOWN
ativo = st.sidebar.selectbox(
    "📊 Escolha o ativo:",
    sorted(lista_ativos)
)

auto_refresh = st.sidebar.checkbox("Atualização automática", True)
intervalo = st.sidebar.slider("Intervalo (segundos)", 10, 120, 30)

if auto_refresh:
    st_autorefresh(interval=intervalo * 1000, key="refresh")

# ========================
# FUNÇÃO DE DADOS
# ========================

def carregar_dados(ativo):
    ticker = yf.Ticker(ativo)
    df = ticker.history(period="1d", interval="1m")
    return df

# ========================
# GRÁFICO DO ATIVO
# ========================

st.subheader(f"📈 {ativo}")

df = carregar_dados(ativo)

if not df.empty:

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, width="stretch")

    ultimo_preco = df["Close"].iloc[-1]
    st.metric("💰 Último preço", f"R$ {round(ultimo_preco, 2)}")

else:
    st.warning("Sem dados.")

# ========================
# SCANNER VISUAL
# ========================

st.subheader("🔥 Top Oportunidades")

if oportunidades:

    df_op = pd.DataFrame(oportunidades)
    df_op = df_op.sort_values(by="score", ascending=False)

    def colorir(val):
        if val >= 7:
            return "color: #00ff00"
        elif val >= 5:
            return "color: yellow"
        else:
            return "color: red"

    st.dataframe(
        df_op.style.applymap(colorir, subset=["score"]),
        use_container_width=True
    )

    top = df_op.iloc[0]

    # ========================
    # DECISÃO COM IA (TRADER)
    # ========================

    st.subheader("🤖 IA Trader (Decisão Profissional)")

    # Se sentimento não estiver funcionando ainda, usamos fallback
    sentimento_simples = "NEUTRO"

    decisao_final = decisao_trade(
        top["ativo"],
        top["score"],
        top["tendencia"],
        top["volume"],
        sentimento_simples
    )

    st.success(decisao_final)

    # ========================
    # MELHOR OPORTUNIDADE
    # ========================

    st.subheader("🧠 Melhor Oportunidade do Momento")

    explicacao = f"""
    Ativo: {top['ativo']}

    📊 Score: {top['score']}
    📈 Tendência: {top['tendencia']}

    📌 Interpretação:
    - Alinhamento entre tendência e volume
    - Possível movimento forte
    """

    st.success(explicacao)

    # ========================
    # NOTÍCIAS
    # ========================

    st.subheader("📰 Notícias do Top Ativo")

    noticias = buscar_noticias(top["ativo"])

    if noticias:

        for n in noticias:
            st.write(f"🗞️ {n['titulo']}")

        sentimento, explicacao_sentimento = analisar_sentimento(noticias)

        st.subheader("📊 Sentimento do Mercado")

        st.success(sentimento)
        st.info(explicacao_sentimento)

    else:
        st.warning("⚠️ Nenhuma notícia encontrada.")

    # ========================
    # DECISÃO
    # ========================

    decisao, analise_ia = gerar_sinal(
        top["ativo"],
        top["score"],
        top["tendencia"],
        top["volume"]
    )

    st.subheader("🎯 Decisão do Sistema")

    st.success(decisao)
    st.info(analise_ia)

    # ========================
    # IA NÍVEL MÁXIMO
    # ========================

    st.subheader("🚀 IA Nível Máximo (Análise Completa)")

    resultado = analise_completa(
        top["ativo"],
        top["score"],
        top["tendencia"],
        top["volume"]
    )

    st.success(resultado)

else:
    st.info("Nenhuma oportunidade detectada.")


# Botão de Teste Manual no Dashboard
if st.sidebar.button("🚀 Testar Alerta Agora"):
    from alerts.telegram_alert import enviar_alerta
    enviar_alerta("🔔 Teste de Conexão: O Radar IA está online e enviando alertas!")
    st.sidebar.success("Alerta enviado para o grupo!")

# ========================
# IA PARA ATIVO ESCOLHIDO
# ========================

st.subheader("🧠 IA Profissional (Ativo Selecionado)")

analise_gpt = analisar_com_gpt(ativo)

st.info(analise_gpt)
