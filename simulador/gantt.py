"""
Este archivo contiene una función sencilla para mostrar
el resultado de la planificación como un diagrama de Gantt
en forma de texto.
"""

def imprimir_gantt(lista_procesos):
    """
    Muestra el orden de ejecución de los procesos en consola,
    simulando un diagrama de Gantt en texto.

    Parámetros:
    - lista_procesos: lista de objetos Proceso con tiempos definidos
    """

    print("\n📊 Diagrama de Gantt:")
    print("Tiempo: ", end="")

    for proceso in lista_procesos:
        for _ in range(proceso.bt):
            print(proceso.pid, end=" ")

    print("\n")
