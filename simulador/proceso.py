class Proceso:
    """
    Clase que representa un proceso en el sistema de planificación.

    Atributos:
    - pid: nombre del proceso (ej. 'P1')
    - bt: Burst Time (tiempo de ejecución)
    - at: Arrival Time (tiempo de llegada)
    - priority: prioridad del proceso
    - remaining_time: tiempo restante (útil para SRT)
    - start_time: momento en que empezó a ejecutarse
    - finish_time: momento en que terminó
    - waiting_time: tiempo total en espera
    - turnaround_time: tiempo total desde llegada hasta finalización
    """
    # Constructor: se usa para crear un nuevo proceso
    def __init__(self, pid, bt, at, priority):
        # Nombre del proceso (como P1, P2...)
        self.pid = pid
        # Tiempo que el proceso necesita para ejecutarse (Burst Time)
        self.bt = int(bt)
        # Tiempo en el que el proceso llega al sistema (Arrival Time)
        self.at = int(at)
        # Prioridad del proceso (menor número = más prioridad)
        self.priority = int(priority)
        # Tiempo restante para ejecutar (solo se usa en algunos algoritmos como SRT)
        self.remaining_time = self.bt
        # Cuándo empieza a ejecutarse por primera vez
        self.start_time = None
        # Cuándo termina de ejecutarse
        self.finish_time = None
        # Cuánto tiempo esperó en la cola antes de ejecutarse
        self.waiting_time = 0
        # Cuánto tiempo pasó desde que llegó hasta que terminó
        self.turnaround_time = 0

    # Método para imprimir los datos del proceso
    def mostrar_info(self):
        print("Proceso:", self.pid)
        print("  Arrival Time:", self.at)
        print("  Burst Time:", self.bt)
        print("  Prioridad:", self.priority)
        print("  Comienza en:", self.start_time)
        print("  Termina en:", self.finish_time)
        print("  Tiempo de espera:", self.waiting_time)
        print("  Tiempo total (turnaround):", self.turnaround_time)
        print("-------------------------------------------")
