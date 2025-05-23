import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import copy
from simulador.cargar_procesos import cargar_procesos_desde_archivo
from simulador.fifo import simular_fifo
from simulador.sjf import simular_sjf
from simulador.rr import simular_rr
from simulador.priority import simular_priority

st.set_page_config(layout="wide")

st.title("Simulador de Algoritmos de Planificación y Sincronización")

tipo_simulacion = st.radio("Selecciona el tipo de simulación", ["Calendarización", "Sincronización"])

if tipo_simulacion == "Calendarización":
    algoritmos = st.multiselect("Selecciona uno o más algoritmos", ["FIFO", "SJF", "Round Robin", "Priority"])
    usar_rr = "Round Robin" in algoritmos
    quantum = None
    if usar_rr:
        quantum = st.number_input("Ingresa el quantum (solo para Round Robin)", min_value=1, max_value=20, value=4, step=1)

    col1, col2 = st.columns(2)
    with col1:
        ejecutar = st.button("Ejecutar simulación")
    with col2:
        limpiar = st.button("Reiniciar")

    if limpiar:
        st.rerun()

    if ejecutar:
        try:
            procesos_base = cargar_procesos_desde_archivo("procesos.txt")

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
                    ax.barh(0, p.bt, left=tiempo, label=p.pid)
                    tiempo += p.bt
                ax.set_yticks([])
                ax.set_xlabel("Tiempo")
                ax.set_title("Gantt")
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=5)
                st.pyplot(fig)

                st.subheader("Tiempo de espera por proceso")
                fig2, ax2 = plt.subplots()
                ax2.bar(df["PID"], df["Waiting"], color='skyblue')
                ax2.set_ylabel("Tiempo de espera")
                ax2.set_xlabel("Proceso")
                ax2.set_title("Tiempos de espera individuales")
                st.pyplot(fig2)

                st.subheader("Tiempo de turnaround por proceso")
                fig3, ax3 = plt.subplots()
                ax3.bar(df["PID"], df["Turnaround"], color='lightgreen')
                ax3.set_ylabel("Turnaround time")
                ax3.set_xlabel("Proceso")
                ax3.set_title("Tiempos de turnaround individuales")
                st.pyplot(fig3)

        except FileNotFoundError:
            st.warning("No se encontró el archivo 'procesos.txt' en el directorio actual.")

else:
    st.subheader("Modo de sincronización")
    modo_sync = st.radio("Selecciona el modo de sincronización", ["Mutex", "Semáforo"])

    archivo_procesos = st.file_uploader("Cargar archivo de procesos (.txt)", type=["txt"], key="procesos_sync")
    archivo_recursos = st.file_uploader("Cargar archivo de recursos (.txt)", type=["txt"], key="recursos")
    archivo_acciones = st.file_uploader("Cargar archivo de acciones (.txt)", type=["txt"], key="acciones")

    if st.button("Simular sincronización"):
        if archivo_procesos and archivo_recursos and archivo_acciones:
            procesos = archivo_procesos.read().decode("utf-8").splitlines()
            recursos = archivo_recursos.read().decode("utf-8").splitlines()
            acciones = archivo_acciones.read().decode("utf-8").splitlines()

            estado_recursos = {}
            for linea in recursos:
                nombre, cantidad = linea.strip().split(',')
                estado_recursos[nombre.strip()] = int(cantidad.strip())

            acciones_organizadas = {}
            for linea in acciones:
                pid, accion, recurso, ciclo = linea.strip().split(',')
                ciclo = int(ciclo.strip())
                if ciclo not in acciones_organizadas:
                    acciones_organizadas[ciclo] = []
                acciones_organizadas[ciclo].append({
                    "pid": pid.strip(),
                    "accion": accion.strip().upper(),
                    "recurso": recurso.strip(),
                    "estado": "PENDING"
                })

            timeline = []
            pendientes = []
            max_ciclo = max(acciones_organizadas.keys()) + 10
            gantt_data = {}

            for ciclo in range(max_ciclo):
                linea = []
                nuevas_pendientes = []
                for a in pendientes:
                    recurso = a["recurso"]
                    pid = a["pid"]
                    if pid not in gantt_data:
                        gantt_data[pid] = {}
                    if estado_recursos[recurso] > 0:
                        estado_recursos[recurso] -= 1
                        a["estado"] = "ACCESSED"
                        linea.append(f"{pid}:{a['accion']}✔")
                        gantt_data[pid][ciclo] = "✔"
                    else:
                        a["estado"] = "WAITING"
                        nuevas_pendientes.append(a)
                        linea.append(f"{pid}:{a['accion']}⌛")
                        gantt_data[pid][ciclo] = "⌛"
                pendientes = nuevas_pendientes

                if ciclo in acciones_organizadas:
                    for a in acciones_organizadas[ciclo]:
                        recurso = a["recurso"]
                        pid = a["pid"]
                        if pid not in gantt_data:
                            gantt_data[pid] = {}
                        if estado_recursos[recurso] > 0:
                            estado_recursos[recurso] -= 1
                            a["estado"] = "ACCESSED"
                            linea.append(f"{pid}:{a['accion']}✔")
                            gantt_data[pid][ciclo] = "✔"
                        else:
                            a["estado"] = "WAITING"
                            pendientes.append(a)
                            linea.append(f"{pid}:{a['accion']}⌛")
                            gantt_data[pid][ciclo] = "⌛"

                timeline.append((ciclo, linea))

            st.subheader("Línea de tiempo de ejecución (ACCESSED / WAITING)")
            for ciclo, acciones in timeline:
                if acciones:
                    st.write(f"Ciclo {ciclo}:", " → ".join(acciones))

            # Visualización tipo Gantt con scroll horizontal
            st.subheader("Visualización por proceso y ciclo")
            if gantt_data:
                ciclos = list(range(max_ciclo))
                gantt_df = pd.DataFrame(index=gantt_data.keys(), columns=[f"C{c}" for c in ciclos])
                for pid, acciones in gantt_data.items():
                    for ciclo in acciones:
                        gantt_df.loc[pid, f"C{ciclo}"] = acciones[ciclo]
                gantt_df.fillna("", inplace=True)
                st.dataframe(gantt_df, use_container_width=True)
        else:
            st.warning("Debes cargar los tres archivos para continuar.")
