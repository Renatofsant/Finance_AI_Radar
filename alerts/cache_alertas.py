alertas_enviados = set()

def ja_enviado(ativo):
    return ativo in alertas_enviados

def marcar_enviado(ativo):
    alertas_enviados.add(ativo)