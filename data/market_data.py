import yfinance as yf

def obter_dados(ativo):

    ticker = yf.Ticker(ativo)

    dados = ticker.history(period="5d", interval="5m")

    if dados.empty:
        return None

    return dados