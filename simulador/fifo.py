"""
Este archivo contiene la función que simula el algoritmo
de planificación First In First Out (FIFO).

Este algoritmo atiende los procesos según el orden en que
llegan (Arrival Time) sin interrupciones.

Requisitos:
- Los procesos deben ser cargados previamente y almacenados
  como objetos de la clase Proceso en una lista.
"""

def simular_fifo(lista_procesos):
    """
    Simula la planificación FIFO.

    Parámetros:
    - lista_procesos: lista de objetos de la clase Proceso

    Retorna:
    - lista_ordenada: lista con los procesos en el orden de ejecución
                      y con sus atributos modificados (tiempos de espera, etc.)
    """

    # Ordenamos los procesos según su tiempo de llegada (Arrival Time)
    lista_procesos.sort(key=lambda proceso: proceso.at)

    # Inicializamos el tiempo actual
    tiempo_actual = 0

    # Creamos una lista para guardar los procesos en el orden en que se ejecutaron
    lista_ordenada = []

    # Recorremos todos los procesos en orden de llegada
    for proceso in lista_procesos:
        # Si el proceso llega después del tiempo actual, debemos esperar
        if proceso.at > tiempo_actual:
            tiempo_actual = proceso.at

        # Guardamos el tiempo en el que empieza a ejecutarse
        proceso.start_time = tiempo_actual

        # Calculamos cuándo termina
        proceso.finish_time = tiempo_actual + proceso.bt

        # Calculamos el tiempo de espera
        proceso.waiting_time = proceso.start_time - proceso.at

        # Calculamos el turnaround time (tiempo total desde llegada hasta finalización)
        proceso.turnaround_time = proceso.finish_time - proceso.at

        # Actualizamos el tiempo actual
        tiempo_actual = proceso.finish_time

        # Agregamos el proceso a la lista de ejecución
        lista_ordenada.append(proceso)

    # Retornamos la lista ordenada con los procesos ya simulados
    return lista_ordenada
