def calcular_score(tendencia, volume, volatilidade):

    score = 0

    if tendencia == "ALTA":
        score += 3

    if volume:
        score += 3

    if volatilidade > 0.02:
        score += 2

    return score