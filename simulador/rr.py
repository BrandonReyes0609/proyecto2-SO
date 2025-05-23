"""
Este archivo contiene la función que simula el algoritmo
de planificación Round Robin (RR).

Round Robin ejecuta los procesos por turnos, cada uno con un tiempo fijo
llamado quantum. Si un proceso no termina durante su quantum, se pone
al final de la cola y espera su próximo turno.

Este algoritmo es preventivo.

Requisitos:
- Los procesos deben estar cargados previamente en una lista.
- Se debe definir el quantum de ejecución.
"""

def simular_rr(lista_procesos, quantum):
    """
    Simula la planificación con Round Robin.

    Parámetros:
    - lista_procesos: lista de objetos de la clase Proceso
    - quantum: cantidad de tiempo que cada proceso puede ejecutar por turno

    Retorna:
    - lista_ordenada: lista de procesos con sus tiempos calculados
                      (waiting_time, turnaround_time, etc.)
    """

    # Tiempo actual de la simulación
    tiempo_actual = 0

    # Procesos que aún no han terminado
    procesos_restantes = lista_procesos.copy()

    # Procesos listos para ejecutar
    queue = []

    # Resultado final con procesos completados
    lista_ordenada = []

    # Para rastrear si un proceso ya ha comenzado (para asignar start_time una sola vez)
    procesos_iniciados = set()

    while len(procesos_restantes) > 0 or len(queue) > 0:

        # Agregamos a la cola los procesos que han llegado
        for proceso in procesos_restantes:
            if proceso.at <= tiempo_actual and proceso not in queue:
                queue.append(proceso)

        # Si no hay nada en la cola, avanzamos el tiempo
        if len(queue) == 0:
            tiempo_actual += 1
            continue

        # Tomamos el primer proceso de la cola
        actual = queue.pop(0)

        # Si es la primera vez que se ejecuta, guardamos su tiempo de inicio
        if actual.pid not in procesos_iniciados:
            actual.start_time = tiempo_actual
            procesos_iniciados.add(actual.pid)

        # Determinamos cuánto tiempo ejecutarlo (quantum o lo que le quede)
        tiempo_ejecucion = min(quantum, actual.remaining_time)

        # Simulamos la ejecución
        tiempo_actual += tiempo_ejecucion
        actual.remaining_time -= tiempo_ejecucion

        # Agregamos nuevos procesos que han llegado durante este quantum
        for proceso in procesos_restantes:
            if proceso.at <= tiempo_actual and proceso not in queue and proceso != actual:
                queue.append(proceso)

        # Si ya terminó, calculamos sus tiempos
        if actual.remaining_time == 0:
            actual.finish_time = tiempo_actual
            actual.turnaround_time = actual.finish_time - actual.at
            actual.waiting_time = actual.turnaround_time - actual.bt
            lista_ordenada.append(actual)
            procesos_restantes.remove(actual)
        else:
            # Si no terminó, lo agregamos al final de la cola
            queue.append(actual)

    return lista_ordenada
