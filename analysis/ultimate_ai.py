from openai import OpenAI
import os
from dotenv import load_dotenv
from analysis.news_analysis import buscar_noticias

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analise_completa(ativo, score, tendencia, volume):

    noticias = buscar_noticias(ativo)

    texto_noticias = ""

    for n in noticias:
        texto_noticias += f"{n['titulo']} - {n['descricao']}\n"

    prompt = f"""
Você é um analista profissional de mercado financeiro.

Analise o ativo {ativo} com base nos dados abaixo:

Tendência: {tendencia}
Score: {score}
Volume forte: {volume}

Notícias:
{texto_noticias}

Responda de forma objetiva:

1. Tendência provável
2. Se é COMPRA, VENDA ou AGUARDAR
3. Justificativa clara
"""

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resposta.choices[0].message.content