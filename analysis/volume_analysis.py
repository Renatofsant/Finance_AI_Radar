def volume_anormal(df):

    df["media_volume"] = df["Volume"].rolling(20).mean()

    volume_atual = df["Volume"].iloc[-1]

    if volume_atual > df["media_volume"].iloc[-1] * 2:
        return True

    return False