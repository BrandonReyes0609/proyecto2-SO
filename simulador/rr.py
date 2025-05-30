"""
Algoritmo de planificación Round Robin (RR).
Cada proceso recibe un tiempo fijo (quantum) para ejecutar. Si no termina, se reencola.
Este algoritmo es preventivo.
"""

from simulador.proceso import Proceso
import copy

def simular_rr(lista_procesos, quantum):
    """
    Simula Round Robin.

    Parámetros:
    - lista_procesos: lista de objetos Proceso
    - quantum: tiempo de ejecución por turno

    Retorna:
    - lista_ordenada: procesos con métricas calculadas
    - ejecucion_por_ciclo: lista de PID por cada ciclo simulado
    """
    procesos = copy.deepcopy(lista_procesos)
    tiempo = 0
    queue = []
    ejecucion_por_ciclo = []
    completados = []
    en_cola = set()

    while len(completados) < len(procesos):
        # Agregar procesos que han llegado
        for p in procesos:
            if p.at <= tiempo and p not in completados and p not in queue and p.remaining_time > 0:
                queue.append(p)
                en_cola.add(p)

        if not queue:
            ejecucion_por_ciclo.append("IDLE")
            tiempo += 1
            continue

        actual = queue.pop(0)
        en_cola.discard(actual)

        if actual.start_time is None:
            actual.start_time = tiempo

        t_ejec = min(quantum, actual.remaining_time)
        for _ in range(t_ejec):
            ejecucion_por_ciclo.append(actual.pid)
            tiempo += 1

            # Durante este tiempo pueden llegar nuevos procesos
            for p in procesos:
                if p.at == tiempo and p not in completados and p not in queue and p.remaining_time > 0:
                    queue.append(p)
                    en_cola.add(p)

        actual.remaining_time -= t_ejec

        if actual.remaining_time == 0:
            actual.finish_time = tiempo
            actual.turnaround_time = actual.finish_time - actual.at
            actual.waiting_time = actual.turnaround_time - actual.bt
            completados.append(actual)
        else:
            queue.append(actual)

    return procesos, ejecucion_por_ciclo
