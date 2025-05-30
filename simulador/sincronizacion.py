
"""
Módulo que simula sincronización usando Mutex o Semáforos.
Procesa acciones desde archivos, gestiona el estado de los recursos,
y devuelve estructuras para visualización tipo Gantt y timeline.
"""

def simular_sincronizacion(procesos_txt, recursos_txt, acciones_txt):
    """
    Simula sincronización de procesos usando acciones de Mutex o Semáforo.

    Parámetros:
    - procesos_txt: lista de líneas del archivo de procesos
    - recursos_txt: lista de líneas del archivo de recursos
    - acciones_txt: lista de líneas del archivo de acciones

    Retorna:
    - timeline: lista de (ciclo, acciones)
    - gantt_data: dict de ciclos por PID con estado ✔ o ⌛
    - max_ciclo: int, cantidad de ciclos simulados
    """

    estado_recursos = {}
    for linea in recursos_txt:
        nombre, cantidad = linea.strip().split(',')
        estado_recursos[nombre.strip()] = int(cantidad.strip())

    acciones_organizadas = {}
    for linea in acciones_txt:
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
                accion = a["accion"]

                if pid not in gantt_data:
                    gantt_data[pid] = {}

                if accion == "SIGNAL":
                    estado_recursos[recurso] += 1
                    linea.append(f"{pid}:SIGNAL🔓")
                    gantt_data[pid][ciclo] = "✔"
                elif estado_recursos[recurso] > 0:
                    estado_recursos[recurso] -= 1
                    a["estado"] = "ACCESSED"
                    linea.append(f"{pid}:{accion}✔")
                    gantt_data[pid][ciclo] = "✔"
                else:
                    a["estado"] = "WAITING"
                    pendientes.append(a)
                    linea.append(f"{pid}:{accion}⌛")
                    gantt_data[pid][ciclo] = "⌛"

        timeline.append((ciclo, linea))

    return timeline, gantt_data, max_ciclo
