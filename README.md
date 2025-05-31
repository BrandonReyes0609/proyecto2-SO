
Realizado por:

- Brandon Javier Reyes Morales 22992

# Simulador de Algoritmos de Planificación y Sincronización

Proyecto final para el curso de **Sistemas Operativos (UVG, 2025)**.
Este simulador permite ejecutar y visualizar dinámicamente algoritmos de **calendarización** de procesos y **mecanismos de sincronización** (mutex y semáforo), utilizando una interfaz gráfica interactiva construida con **Streamlit**.

---

## Estructura del Proyecto

```
proyecto2-SO/
├── app.py
├── simulador/
│   ├── cargar_procesos.py
│   ├── fifo.py
│   ├── sjf.py
│   ├── srt.py
│   ├── rr.py
│   ├── priority.py
│   ├── mutex.py
│   ├── semaforo.py
│   └── gantt.py
├── procesos_sync_var.txt
├── recursos_sync_var.txt
├── acciones_mutex_var.txt
├── acciones_semaforo_var.txt
├── README.md
```

---

## ¿Cómo ejecutar el simulador?

1. Instala dependencias:

```bash
pip install streamlit pandas matplotlib
```

2. Ejecuta la aplicación desde terminal:

```bash
streamlit run app.py
```

---

## Archivos necesarios para ejecutar simulaciones

### A. Simulación de Calendarización

Debes cargar un archivo `.txt` con los procesos, con el siguiente formato por línea:

```
<PID>, <BT>, <AT>, <PRIORIDAD>
Ejemplo: P1, 8, 0, 1
```

### B. Simulación de Sincronización

Debes cargar tres archivos `.txt`:

1. **Procesos**

```
<PID>, <BT>, <AT>, <PRIORIDAD>
```

2. **Recursos**

```
<NOMBRE_RECURSO>, <CONTADOR>
Ejemplo: R1, 1
```

3. **Acciones**

- Para **mutex**: `acciones_mutex_var.txt`
- Para **semáforo**: `acciones_semaforo_var.txt`

```
<PID>, <ACCION>, <RECURSO>, <CICLO>
Ejemplo: P1, READ, R1, 0
```

---

## ⚙️ Algoritmos Soportados

### Calendarización

- First In First Out (FIFO)
- Shortest Job First (SJF)
- Shortest Remaining Time (SRT)
- Round Robin (configurable)
- Priority

### Sincronización

- Mutex Locks
- Semáforos

---

## Resultados

El simulador muestra gráficamente:

- Línea de tiempo por proceso (diagrama de Gantt).
- Estados dinámicos por ciclo (`WAITING`, `ACCESSED`).
- Métricas como **tiempo promedio de espera** y **turnaround**.

---

## Requerimientos del curso cubiertos

 Simulación visual dinámica
✔️ Carga desde archivos `.txt`
✔️ Implementación de algoritmos clásicos
✔️ Interfaz interactiva y amigable
✔️ Cálculo de métricas de eficiencia
✔️ Animación por ciclos con scroll horizontal

---

## Referencias

- Silberschatz, A. (2018). *Operating System Concepts*.
- Stallings, W. (2018). *Operating Systems: Internals and Design Principles*.
- Tanenbaum, A. (2015). *Modern Operating Systems*.
- García Zarceño, J. L. (2025). *Temas de Sistemas Operativos*, UVG.

---

 *Universidad del Valle de Guatemala – 2025*
