
# Proyecto 2 - Simulador de Algoritmos de Planificación y Sincronización

Este proyecto es una aplicación interactiva construida con Streamlit que simula algoritmos de **calendarización** (planificación) y **sincronización** de procesos. Fue desarrollado como parte del curso de Sistemas Operativos.

---

## 📁 Estructura del Proyecto

```
proyecto2-SO/
├── app.py                    # Interfaz principal Streamlit
├── main.py                   # Entrada alternativa para pruebas de calendarización
├── simulador/                # Lógica de simulación
│   ├── fifo.py
│   ├── sjf.py
│   ├── rr.py
│   ├── priority.py
│   ├── proceso.py
│   ├── cargar_procesos.py
│   ├── metricas.py
│   ├── gantt.py
│   └── __init__.py
├── data/                     # Archivos de procesos por algoritmo
│   ├── procesos.txt
│   ├── procesos_FIFO.txt
│   ├── procesos_SJF.txt
│   └── procesos_temp.txt
├── files/                    # Archivos para simulación de sincronización
│   ├── procesos.txt
│   ├── recursos.txt
│   └── acciones.txt
├── docs/                     # Documentación y entregables
│   └── Definición de Proyecto Simulador 2025.pdf
├── README.md
└── requirements.txt
```

---

## 🚀 Cómo ejecutar

### Requisitos

- Python 3.8+
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Ejecutar la app con Streamlit

```bash
streamlit run app.py
```

---

## 🔧 Funcionalidades

### A. Simulación de Calendarización
- Algoritmos: FIFO, SJF, Round Robin (con quantum), Priority.
- Métricas: Tiempo de espera y turnaround.
- Visualización: Diagrama de Gantt + gráficos de barras.
- Comparación simultánea de múltiples algoritmos.

### B. Simulación de Sincronización
- Modos: Mutex y Semáforo.
- Archivos cargables: procesos, recursos, acciones.
- Visualización dinámica:
  - Línea de tiempo por ciclo
  - Tabla con scroll horizontal por proceso y ciclo
  - Estados: ✔ ACCESSED, ⌛ WAITING

---

## 📦 Créditos
Desarrollado por: [Tu Nombre]  
Curso: Sistemas Operativos  
Universidad: Universidad del Valle de Guatemala

