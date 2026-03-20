from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def decisao_trade(ativo, score, tendencia, volume, sentimento):

    try:

        prompt = f"""
        Você é um trader profissional experiente.

        Analise os dados abaixo e tome uma decisão:

        Ativo: {ativo}
        Score: {score}
        Tendência: {tendencia}
        Volume: {volume}
        Sentimento: {sentimento}

        Escolha APENAS uma opção:
        - ENTRAR
        - SAIR
        - ESPERAR

        Depois explique rapidamente o motivo.

        Formato da resposta:

        DECISÃO: (ENTRAR, SAIR ou ESPERAR)
        MOTIVO: explicação
        """

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um trader institucional."},
                {"role": "user", "content": prompt}
            ]
        )

        texto = resposta.choices[0].message.content

        return texto

    except Exception as e:
        return f"Erro na decisão: {e}"