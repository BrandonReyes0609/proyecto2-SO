import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import copy
from simulador.cargar_procesos import cargar_procesos_desde_archivo
from simulador.fifo import simular_fifo
from simulador.sjf import simular_sjf
from simulador.rr import simular_rr
from simulador.priority import simular_priority
from simulador.srt import simular_srt
from simulador.gantt import dibujar_gantt_por_ciclo
#from simulador.sincronizacion import simular_sincronizacion
from simulador.sincronizacion_mutex import simular_mutex
from simulador.sincronizacion_semaforo import simular_semaforo

st.set_page_config(layout="wide")

st.title("Simulador de Algoritmos de Planificación y Sincronización")

tipo_simulacion = st.radio("Selecciona el tipo de simulación", ["Calendarización", "Sincronización"])

if tipo_simulacion == "Calendarización":
    algoritmos = st.multiselect("Selecciona uno o más algoritmos", ["FIFO", "SJF", "Round Robin", "Priority","srt"])
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
            procesos_base = cargar_procesos_desde_archivo("data/procesos.txt")

            for algoritmo in algoritmos:
                st.subheader(f"Resultado: {algoritmo}")
                procesos = copy.deepcopy(procesos_base)

                ejecucion_ciclica = []
                if algoritmo == "FIFO":
                    resultado = simular_fifo(procesos)
                    for p in resultado:
                        ejecucion_ciclica += [p.pid] * p.bt
                elif algoritmo == "SJF":
                    resultado = simular_sjf(procesos)
                    for p in resultado:
                        ejecucion_ciclica += [p.pid] * p.bt
                elif algoritmo == "Round Robin":
                    resultado, ejecucion_ciclica = simular_rr(procesos, quantum)
                elif algoritmo == "Priority":
                    resultado = simular_priority(procesos)
                    for p in resultado:
                        ejecucion_ciclica += [p.pid] * p.bt
                elif algoritmo == "srt":
                    resultado, ejecucion_ciclica = simular_srt(procesos)
                else:
                    st.warning("Algoritmo no reconocido")
                    continue

                data = [{
                    "PID": p.pid,
                    "AT": f"{p.at:.2f}",
                    "BT": f"{p.bt:.2f}",
                    "Priority": f"{p.priority:.2f}",
                    "Start": f"{p.start_time:.2f}",
                    "Finish": f"{p.finish_time:.2f}",
                    "Waiting": f"{p.waiting_time:.2f}",
                    "Turnaround": f"{p.turnaround_time:.2f}"
                } for p in resultado]

                df = pd.DataFrame(data)
                st.dataframe(df)

                promedio_espera = sum([p.waiting_time for p in resultado]) / len(resultado)
                promedio_turnaround = sum([p.turnaround_time for p in resultado]) / len(resultado)

                st.success(f"Tiempo promedio de espera: {promedio_espera:.2f}")
                st.success(f"Tiempo promedio de turnaround: {promedio_turnaround:.2f}")

                st.subheader("Diagrama de Gantt")
                if ejecucion_ciclica:
                    fig = dibujar_gantt_por_ciclo(ejecucion_ciclica, titulo=f"Gantt: {algoritmo}")
                    st.pyplot(fig)
                else:
                    st.info("Este algoritmo no tiene ejecución por ciclo o no fue generado correctamente.")

                #--------------------
                st.subheader("Tiempo de espera por proceso")
                fig2, ax2 = plt.subplots(figsize=(5, 2.5))
                ax2.bar([p.pid for p in resultado], [p.waiting_time for p in resultado], color='skyblue')
                ax2.set_ylabel("Tiempo de espera")
                ax2.set_xlabel("Proceso")
                ax2.set_title("Tiempos de espera individuales")
                fig2.tight_layout()
                st.pyplot(fig2, bbox_inches="tight")

                st.subheader("Tiempo de turnaround por proceso")
                fig3, ax3 = plt.subplots(figsize=(5, 2.5))
                ax3.bar([p.pid for p in resultado], [p.turnaround_time for p in resultado], color='lightgreen')
                ax3.set_ylabel("Turnaround time")
                ax3.set_xlabel("Proceso")
                ax3.set_title("Tiempos de turnaround individuales")
                fig3.tight_layout()
                st.pyplot(fig3, bbox_inches="tight")

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
            procesos_txt = archivo_procesos.read().decode("utf-8").splitlines()
            recursos_txt = archivo_recursos.read().decode("utf-8").splitlines()
            acciones_txt = archivo_acciones.read().decode("utf-8").splitlines()

            #timeline, gantt_data, max_ciclo = simular_sincronizacion(procesos_txt, recursos_txt, acciones_txt)

            if modo_sync == "Mutex":
                timeline, gantt_data, max_ciclo = simular_mutex(procesos_txt, recursos_txt, acciones_txt)
            else:
                timeline, gantt_data, max_ciclo = simular_semaforo(procesos_txt, recursos_txt, acciones_txt)

            st.subheader("Línea de tiempo de ejecución (ACCESSED / WAITING)")
            for ciclo, acciones in timeline:
                if acciones:
                    st.write(f"Ciclo {ciclo}:", " → ".join(acciones))

            st.subheader("Visualización por proceso y ciclo (dinámica)")
            if gantt_data:
                ciclos = list(range(max_ciclo))
                colores = {"✔": "#00CC44", "⌛": "#24702D", "": "#FFFFFF"}
                tabla = """<style>
                table {border-collapse: collapse; width: 100%; font-size: 11px;}
                th, td {border: 1px solid #ddd; text-align: center; padding: 4px;}
                .green {background-color: #00CC44; color: white;}
                .orange {background-color: #FFA500; color: black;}
                </style><table><thead><tr><th>PID</th>"""
                tabla += "".join([f"<th>C{c}</th>" for c in ciclos]) + "</tr></thead><tbody>"
                for pid in gantt_data:
                    tabla += f"<tr><td><b>{pid}</b></td>"
                    for c in ciclos:
                        estado = gantt_data[pid].get(c, "")
                        color_class = "green" if estado == "✔" else "orange" if estado == "⌛" else ""
                        tabla += f"<td class='{color_class}'>{estado}</td>"
                    tabla += "</tr>"
                tabla += "</tbody></table>"
                st.markdown(tabla, unsafe_allow_html=True)

            st.subheader("Estado dinámico animado (máx. 3 procesos)")
            if gantt_data:
                import streamlit.components.v1 as components
                procesos = list(gantt_data.keys())[:3]

                max_ciclo = max([max(v.keys()) if v else 0 for v in gantt_data.values()]) + 1

                html_anim = f"""
                <style>
                .cuadro {{
                    width: 100px;
                    height: 100px;
                    display: inline-block;
                    margin: 5px;
                    border-radius: 10px;
                }}
                .etiqueta {{
                    text-align: center;
                    margin-top: 5px;
                    font-weight: bold;
                }}
                </style>
                <div id='contenedor'>
                """

                for pid in procesos:
                    html_anim += f"<div class='etiqueta'>{pid}</div>"
                    html_anim += f"<div id='cuadro_{pid}' class='cuadro' style='background:#CCC;'></div>"

                html_anim += "</div><script>\n"
                html_anim += f"const maxCiclo = {max_ciclo};\nlet ciclo = 0;\nconst interval = 500;\n"

                for pid in procesos:
                    estados = []
                    for c in range(max_ciclo):
                        estado = gantt_data[pid].get(c, "")
                        color = "#00CC44" if estado == "✔" else "#FFA500" if estado == "⌛" else "#CCCCCC"
                        estados.append(f'"{color}"')
                    html_anim += f"const {pid} = [{','.join(estados)}];\n"

                html_anim += """
                function actualizar() {
                    ciclo = (ciclo + 1) % maxCiclo;\n"""
                for pid in procesos:
                    html_anim += f"document.getElementById('cuadro_{pid}').style.background = {pid}[ciclo];\n"
                html_anim += """
                }
                setInterval(actualizar, interval);
                actualizar();
                </script>
                """

                components.html(html_anim, height=250)


        else:
            st.warning("Debes cargar los tres archivos para continuar.")
