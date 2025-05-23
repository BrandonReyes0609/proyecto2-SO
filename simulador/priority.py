"""
Este archivo contiene la función que simula el algoritmo
de planificación por prioridad (Priority Scheduling).

Este algoritmo selecciona, entre los procesos disponibles,
el que tenga la prioridad más alta (menor número).

Es no preventivo: una vez que un proceso inicia su ejecución,
no se interrumpe hasta que termina.

Requisitos:
- Los procesos deben tener definido un campo de prioridad.
"""

def simular_priority(lista_procesos):
    """
    Simula la planificación con el algoritmo de prioridad (no preventivo).

    Parámetros:
    - lista_procesos: lista de objetos de la clase Proceso

    Retorna:
    - lista_ordenada: lista con los procesos en el orden en que fueron ejecutados
                      y con sus tiempos calculados (start, finish, wait, turnaround)
    """

    # Tiempo actual del sistema
    tiempo_actual = 0

    # Lista de procesos restantes (aún no ejecutados)
    procesos_restantes = lista_procesos.copy()

    # Lista de procesos ya ejecutados en orden
    lista_ordenada = []

    while len(procesos_restantes) > 0:
        # Filtrar procesos que ya han llegado
        candidatos = []
        for p in procesos_restantes:
            if p.at <= tiempo_actual:
                candidatos.append(p)

        # Si no hay procesos listos, avanzar el tiempo
        if len(candidatos) == 0:
            tiempo_actual += 1
            continue

        # Elegir el proceso con prioridad más alta (menor número)
        proceso_seleccionado = candidatos[0]
        for p in candidatos:
            if p.priority < proceso_seleccionado.priority:
                proceso_seleccionado = p
            elif p.priority == proceso_seleccionado.priority:
                # En caso de empate, se elige el que llegó antes
                if p.at < proceso_seleccionado.at:
                    proceso_seleccionado = p

        # Asignar tiempos
        proceso_seleccionado.start_time = tiempo_actual
        proceso_seleccionado.finish_time = tiempo_actual + proceso_seleccionado.bt
        proceso_seleccionado.waiting_time = proceso_seleccionado.start_time - proceso_seleccionado.at
        proceso_seleccionado.turnaround_time = proceso_seleccionado.finish_time - proceso_seleccionado.at

        # Avanzar el tiempo
        tiempo_actual = proceso_seleccionado.finish_time

        # Agregar a la lista de completados y quitarlo de los restantes
        lista_ordenada.append(proceso_seleccionado)
        procesos_restantes.remove(proceso_seleccionado)

    return lista_ordenada
