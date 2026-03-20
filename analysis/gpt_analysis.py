from openai import OpenAI
import os
from dotenv import load_dotenv
from analysis.news_analysis import buscar_noticias

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analisar_com_gpt(ativo):

    noticias = buscar_noticias(ativo)

    # 🔥 VERIFICA SE VEIO NOTÍCIA
    if not noticias:
        return "⚠️ Nenhuma notícia encontrada no momento."

    texto_noticias = ""

    for n in noticias:
        titulo = n.get("titulo", "")
        descricao = n.get("descricao", "")

        texto_noticias += f"Título: {titulo}\nDescrição: {descricao}\n\n"

    prompt = f"""
Você é um analista financeiro profissional.

Analise APENAS as notícias abaixo e diga o que pode acontecer com o ativo {ativo}.

Seja direto, objetivo e específico.

Notícias:
{texto_noticias}

Responda com:
- Tendência provável (Alta, Baixa ou Neutra)
- Motivo claro baseado nas notícias
"""

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resposta.choices[0].message.content