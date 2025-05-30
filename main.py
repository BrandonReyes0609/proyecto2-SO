import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import copy
from simulador.cargar_procesos import cargar_procesos_desde_archivo
from simulador.fifo import simular_fifo
from simulador.sjf import simular_sjf
from simulador.rr import simular_rr
from simulador.priority import simular_priority
from simulador.srt import simular_srt  # NUEVO

st.set_page_config(layout="wide")
st.title("Simulador de Algoritmos de Planificación y Sincronización")

tipo_simulacion = st.radio("Selecciona el tipo de simulación", ["Calendarización", "Sincronización"])

if tipo_simulacion == "Calendarización":
    algoritmos = st.multiselect("Selecciona uno o más algoritmos", ["FIFO", "SJF", "Round Robin", "Priority", "SRT"])
    usar_rr = "Round Robin" in algoritmos
    quantum = None
    if usar_rr:
        quantum = st.number_input("Ingresa el quantum (solo para Round Robin)", min_value=1, max_value=20, value=4)

    col1, col2 = st.columns(2)
    with col1:
        ejecutar = st.button("Ejecutar simulación")
    with col2:
        limpiar = st.button("Reiniciar")

    if limpiar:
        st.rerun()

    if ejecutar:
        try:
            procesos_base = cargar_procesos_desde_archivo("data/procesos.txt")

            for algoritmo in algoritmos:
                st.subheader(f"Resultado: {algoritmo}")
                procesos = copy.deepcopy(procesos_base)

                if algoritmo == "FIFO":
                    resultado = simular_fifo(procesos)
                elif algoritmo == "SJF":
                    resultado = simular_sjf(procesos)
                elif algoritmo == "Round Robin":
                    resultado = simular_rr(procesos, quantum)
                elif algoritmo == "Priority":
                    resultado = simular_priority(procesos)
                elif algoritmo == "SRT":
                    resultado, _ = simular_srt(procesos)
                else:
                    st.warning("Algoritmo no reconocido")
                    continue

                data = [{
                    "PID": p.pid,
                    "AT": p.at,
                    "BT": p.bt,
                    "Priority": p.priority,
                    "Start": p.start_time,
                    "Finish": p.finish_time,
                    "Waiting": p.waiting_time,
                    "Turnaround": p.turnaround_time
                } for p in resultado]

                df = pd.DataFrame(data)
                st.dataframe(df)

                promedio_espera = df["Waiting"].mean()
                promedio_turnaround = df["Turnaround"].mean()

                st.success(f"Tiempo promedio de espera: {promedio_espera:.2f}")
                st.success(f"Tiempo promedio de turnaround: {promedio_turnaround:.2f}")

                st.subheader("Diagrama de Gantt")
                fig, ax = plt.subplots(figsize=(10, 2))
                tiempo = 0
                for p in resultado:
                    ax.barh(0, p.bt, left=p.start_time or tiempo, label=p.pid)
                    tiempo = (p.start_time or tiempo) + p.bt
                ax.set_yticks([])
                ax.set_xlabel("Tiempo")
                ax.set_title("Gantt")
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=5)
                st.pyplot(fig)

        except FileNotFoundError:
            st.warning("No se encontró el archivo 'procesos.txt'.")
