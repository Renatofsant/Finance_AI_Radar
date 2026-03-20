def detectar_tendencia(df):

    df["media20"] = df["Close"].rolling(20).mean()
    df["media50"] = df["Close"].rolling(50).mean()

    ultimo = df.iloc[-1]

    if ultimo["media20"] > ultimo["media50"]:
        return "ALTA"

    elif ultimo["media20"] < ultimo["media50"]:
        return "BAIXA"

    return "NEUTRO"