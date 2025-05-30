"""
Algoritmo Shortest Remaining Time (SRT).
Algoritmo preventivo que siempre elige el proceso con menor tiempo restante.
"""

from simulador.proceso import Proceso
import copy

def simular_srt(lista_procesos):
    """
    Simula SRT paso a paso.

    Parámetros:
    - lista_procesos: lista de objetos Proceso

    Retorna:
    - procesos: lista con métricas completas
    - ejecucion_por_ciclo: lista con PID ejecutado en cada ciclo
    """
    procesos = copy.deepcopy(lista_procesos)
    tiempo = 0
    completados = 0
    n = len(procesos)
    ejecucion_por_ciclo = []

    while completados < n:
        candidatos = [p for p in procesos if p.at <= tiempo and p.remaining_time > 0]
        if candidatos:
            actual = min(candidatos, key=lambda p: p.remaining_time)

            if actual.start_time is None:
                actual.start_time = tiempo

            actual.remaining_time -= 1
            ejecucion_por_ciclo.append(actual.pid)
            tiempo += 1

            if actual.remaining_time == 0:
                actual.finish_time = tiempo
                actual.turnaround_time = actual.finish_time - actual.at
                actual.waiting_time = actual.turnaround_time - actual.bt
                completados += 1
        else:
            ejecucion_por_ciclo.append("IDLE")
            tiempo += 1

    return procesos, ejecucion_por_ciclo
