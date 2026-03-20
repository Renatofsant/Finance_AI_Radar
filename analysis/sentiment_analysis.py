from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analisar_sentimento(noticias):

    try:

        if not noticias:
            return "🟡 NEUTRO", "Sem notícias relevantes no momento."

        textos = "\n".join([n["titulo"] for n in noticias if n["titulo"]])

        if not textos.strip():
            return "🟡 NEUTRO", "Notícias sem conteúdo relevante."

        prompt = f"""
        Você é um analista de mercado financeiro profissional.

        Com base nas notícias abaixo, diga o sentimento geral do mercado.

        Responda EXATAMENTE neste formato:

        SENTIMENTO: POSITIVO ou NEGATIVO ou NEUTRO
        EXPLICAÇÃO: breve explicação

        Notícias:
        {textos}
        """

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um analista financeiro especialista."},
                {"role": "user", "content": prompt}
            ]
        )

        texto = resposta.choices[0].message.content

        if not texto:
            return "🟡 NEUTRO", "IA não retornou resposta."

        texto_upper = texto.upper()

        if "POSITIVO" in texto_upper:
            return "🟢 POSITIVO", texto
        elif "NEGATIVO" in texto_upper:
            return "🔴 NEGATIVO", texto
        else:
            return "🟡 NEUTRO", texto

    except Exception as e:
        return "⚠️ ERRO", f"Erro na análise de sentimento: {e}"