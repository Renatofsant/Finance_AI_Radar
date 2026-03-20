from scheduler.market_scanner import escanear


def radar():

    oportunidades = escanear()

    print("\n📊 OPORTUNIDADES DETECTADAS\n")

    if not oportunidades:
        print("Nenhuma oportunidade encontrada.")
        return

    oportunidades = sorted(oportunidades, key=lambda x: x["score"], reverse=True)

    for op in oportunidades:

        print(f"""
Ativo: {op['ativo']}
Score: {op['score']}
Tendência: {op['tendencia']}
Volume Anormal: {op['volume']}
Volatilidade: {op['volatilidade']}
-----------------------------
""")