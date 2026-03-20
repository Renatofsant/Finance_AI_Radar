from data.assets_database import obter_todos_ativos
from data.market_data import obter_dados

from analysis.technical_analysis import detectar_tendencia
from analysis.volume_analysis import volume_anormal
from analysis.volatility_analysis import calcular_volatilidade
from analysis.opportunity_score import calcular_score
from alerts.cache_alertas import ja_enviado, marcar_enviado

from alerts.telegram_alert import enviar_alerta

# Controle para evitar spam
ativos_alertados = set()


def escanear():

    ativos = obter_todos_ativos()

    oportunidades = []

    for ativo in ativos:

        try:

            df = obter_dados(ativo)

            if df is None:
                continue

            tendencia = detectar_tendencia(df)
            volume = volume_anormal(df)
            volatilidade = calcular_volatilidade(df)

            score = calcular_score(tendencia, volume, volatilidade)

            if score >=5:

                if not ja_enviado(ativo):
                    mensagem = f"""
            🚨 OPORTUNIDADE DETECTADA

            Ativo: {ativo}
            Score: {score}
            Tendência: {tendencia}
            Volume forte: {volume}
            """

                    enviar_alerta(mensagem)

                    marcar_enviado(ativo)

                oportunidades.append({
                    "ativo": ativo,
                    "score": score,
                    "tendencia": tendencia,
                    "volume": volume,
                    "volatilidade": round(volatilidade, 4)
                })


                # 🚀 ENVIO DE ALERTA (SEM SPAM)
                if ativo not in ativos_alertados:

                    mensagem = f"""
🔥 OPORTUNIDADE FORTE DETECTADA

📊 Ativo: {ativo}
📈 Tendência: {tendencia}
⚡ Score: {score}
📉 Volatilidade: {round(volatilidade, 4)}

🧠 Possível entrada institucional detectada.
"""

                    enviar_alerta(mensagem)

                    ativos_alertados.add(ativo)

        except Exception as e:
            print(f"Erro no ativo {ativo}: {e}")

    return oportunidades