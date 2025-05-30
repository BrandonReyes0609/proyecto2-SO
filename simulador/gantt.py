"""
Este archivo contiene una función sencilla para mostrar
el resultado de la planificación como un diagrama de Gantt
en forma de texto.
"""


import matplotlib.pyplot as plt
from matplotlib import colors as mcolors


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


def dibujar_gantt_por_ciclo(lista_ciclica, titulo="Diagrama de Gantt"):
    """
    Dibuja un diagrama de Gantt basado en una lista de ejecución por ciclo.

    Parámetros:
    - lista_ciclica: lista de pids por cada ciclo de ejecución (["P1", "P1", "P2", ...])
    - titulo: título que se mostrará en la gráfica

    Retorna:
    - fig: figura de matplotlib lista para ser renderizada con st.pyplot(fig)
    """
    colores = list(mcolors.TABLEAU_COLORS.values())
    mapa_procesos = {}
    fig, ax = plt.subplots(figsize=(10, 1.2))

    for i, pid in enumerate(lista_ciclica):
        if pid not in mapa_procesos:
            mapa_procesos[pid] = colores[len(mapa_procesos) % len(colores)]
        color = "lightgray" if pid == "IDLE" else mapa_procesos[pid]
        ax.barh(0, 1, left=i, height=0.5, color=color, edgecolor='black')
        ax.text(i + 0.5, 0, pid, ha='center', va='center', fontsize=6)

    ax.set_xlim(0, len(lista_ciclica))
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xticks(range(len(lista_ciclica)))
    ax.set_xlabel("Ciclo")
    ax.set_title(titulo)
    fig.tight_layout()
    return fig

