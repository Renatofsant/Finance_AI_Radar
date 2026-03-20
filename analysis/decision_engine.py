from analysis.gpt_analysis import analisar_com_gpt

def gerar_sinal(ativo, score, tendencia, volume):

    analise_ia = analisar_com_gpt(ativo)

    if score >= 7 and tendencia == "ALTA" and volume:
        decisao = "📈 COMPRA FORTE"

    elif score >= 7 and tendencia == "BAIXA":
        decisao = "📉 VENDA / SAÍDA"

    else:
        decisao = "⚖️ AGUARDAR"

    return decisao, analise_ia