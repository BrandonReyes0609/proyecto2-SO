"""
Este archivo contiene la función que simula el algoritmo
de planificación Shortest Job First (SJF).

SJF selecciona el proceso con el menor tiempo de ejecución (BT)
de entre los procesos que ya han llegado (AT <= tiempo actual).

Este algoritmo no es preventivo.

Requisitos:
- Los procesos deben estar cargados previamente en una lista.
"""

def simular_sjf(lista_procesos):
    """
    Simula la planificación con el algoritmo Shortest Job First.

    Parámetros:
    - lista_procesos: lista de objetos de la clase Proceso

    Retorna:
    - lista_ordenada: lista de procesos en el orden en que fueron ejecutados,
                      con sus tiempos de inicio, espera y finalización calculados.
    """

    # Lista donde se colocarán los procesos que ya se ejecutaron
    lista_ordenada = []

    # Tiempo actual en la simulación
    tiempo_actual = 0

    # Lista de procesos que todavía no se han ejecutado
    procesos_restantes = lista_procesos.copy()

    while len(procesos_restantes) > 0:
        # Buscamos todos los procesos que han llegado (AT <= tiempo_actual)
        candidatos = []
        for proceso in procesos_restantes:
            if proceso.at <= tiempo_actual:
                candidatos.append(proceso)

        # Si no hay candidatos, el sistema debe esperar hasta que llegue uno
        if len(candidatos) == 0:
            tiempo_actual += 1
            continue

        # Buscamos el proceso con el menor Burst Time (BT)
        proceso_seleccionado = candidatos[0]
        for p in candidatos:
            if p.bt < proceso_seleccionado.bt:
                proceso_seleccionado = p

        # Calculamos tiempos
        proceso_seleccionado.start_time = tiempo_actual
        proceso_seleccionado.finish_time = tiempo_actual + proceso_seleccionado.bt
        proceso_seleccionado.waiting_time = proceso_seleccionado.start_time - proceso_seleccionado.at
        proceso_seleccionado.turnaround_time = proceso_seleccionado.finish_time - proceso_seleccionado.at

        # Avanzamos el tiempo
        tiempo_actual = proceso_seleccionado.finish_time

        # Añadimos el proceso a la lista ordenada y lo quitamos de los restantes
        lista_ordenada.append(proceso_seleccionado)
        procesos_restantes.remove(proceso_seleccionado)

    return lista_ordenada
