"""
Este archivo contiene funciones para calcular y mostrar
las métricas de eficiencia del algoritmo de planificación.

Métricas:
- Tiempo promedio de espera (Average Waiting Time)
- Tiempo promedio de turnaround (Average Turnaround Time)
"""

def calcular_metricas(lista_procesos):
    """
    Calcula y muestra las métricas de eficiencia del algoritmo.

    Parámetros:
    - lista_procesos: lista con objetos de la clase Proceso
                      que ya fueron ejecutados (con tiempos asignados)
    """

    # Inicializamos acumuladores
    suma_espera = 0
    suma_turnaround = 0

    # Recorremos todos los procesos y sumamos sus tiempos
    for proceso in lista_procesos:
        suma_espera += proceso.waiting_time
        suma_turnaround += proceso.turnaround_time

    # Calculamos los promedios
    cantidad = len(lista_procesos)

    if cantidad > 0:
        promedio_espera = suma_espera / cantidad
        promedio_turnaround = suma_turnaround / cantidad

        # Mostramos los resultados
        print(f"📈 Tiempo promedio de espera: {promedio_espera:.2f}")
        print(f"📈 Tiempo promedio de turnaround: {promedio_turnaround:.2f}")
    else:
        print("⚠️ No hay procesos para calcular métricas.")
