"""
Este es el archivo principal que integra:
- Carga de procesos desde archivo
- Simulación FIFO
- Visualización de resultados
"""

from simulador.cargar_procesos import cargar_procesos_desde_archivo
from simulador.fifo import simular_fifo
from simulador.sjf import simular_sjf
from simulador.rr import simular_rr
from simulador.priority import simular_priority
from simulador.metricas import calcular_metricas
from simulador.gantt import imprimir_gantt

# Cargar procesos desde archivo
#procesos = cargar_procesos_desde_archivo("procesos_FIFO.txt")
procesos = cargar_procesos_desde_archivo("files/procesos.txt")

# Simular el algoritmo FIFO
print("----Simulación FIFO ----")
procesos_ejecutados = simular_fifo(procesos)

# Mostrar resultados
for proceso in procesos_ejecutados:
    proceso.mostrar_info()

# Mostrar diagrama de Gantt
print("\n📊 Diagrama de Gantt:")
imprimir_gantt(procesos_ejecutados)
print("\n")
# Calcular y mostrar métricas
calcular_metricas(procesos_ejecutados)


procesos = cargar_procesos_desde_archivo("files/procesos.txt")
print("----Simulación SJF ----")
procesos_ejecutados = simular_sjf(procesos)

# Mostrar resultados de SJF
for proceso in procesos_ejecutados:
    proceso.mostrar_info()

# Mostrar diagrama de Gantt de SJF
print("\n📊 Diagrama de Gantt:")
imprimir_gantt(procesos_ejecutados)

# Calcular y mostrar métricas de SJF
calcular_metricas(procesos_ejecutados)


print("----Simulación Round Robin (Quantum = 4) ----")
procesos = cargar_procesos_desde_archivo("files/procesos.txt")
procesos_rr = simular_rr(procesos, quantum=4)

for p in procesos_rr:
    p.mostrar_info()

imprimir_gantt(procesos_rr)
calcular_metricas(procesos_rr)



print("----Simulación Priority Scheduling ----")
procesos = cargar_procesos_desde_archivo("files/procesos.txt")
procesos_priority = simular_priority(procesos)

for p in procesos_priority:
    p.mostrar_info()

imprimir_gantt(procesos_priority)
calcular_metricas(procesos_priority)
