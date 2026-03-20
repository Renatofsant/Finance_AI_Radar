import time
from scheduler.radar import radar
from config import INTERVALO_ANALISE

print("🚀 SISTEMA DE IA DE MERCADO INICIADO\n")

while True:

    radar()

    print("\n⏳ Aguardando próxima análise...\n")

    time.sleep(INTERVALO_ANALISE)