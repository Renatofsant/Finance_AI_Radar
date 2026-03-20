import numpy as np

def calcular_volatilidade(df):

    df["retorno"] = df["Close"].pct_change()

    vol = np.std(df["retorno"])

    return vol