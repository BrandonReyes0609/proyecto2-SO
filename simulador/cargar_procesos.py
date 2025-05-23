"""
Este archivo contiene la función para leer un archivo de texto (.txt)
y cargar una lista de procesos.

Formato de archivo por línea:
<PID>, <BT>, <AT>, <PRIORITY>

Ejemplo:
P1, 8, 0, 1
P2, 4, 1, 2
P3, 5, 2, 3
"""

# Importar la clase Proceso definida en proceso.py
from .proceso import Proceso

def cargar_procesos_desde_archivo(nombre_archivo):
    """
    Función que lee un archivo con la lista de procesos
    y devuelve una lista de objetos de la clase Proceso.

    Parámetros:
    - nombre_archivo: nombre del archivo de texto (string)

    Retorna:
    - lista_procesos: lista con objetos Proceso cargados
    """

    # Creamos una lista vacía para guardar los procesos
    lista_procesos = []

    try:
        # Abrimos el archivo en modo lectura
        archivo = open(nombre_archivo, 'r')

        # Leemos todas las líneas del archivo
        lineas = archivo.readlines()

        # Recorremos cada línea del archivo
        for linea in lineas:
            # Quitamos los espacios y el salto de línea
            linea = linea.strip()

            # Dividimos la línea usando la coma como separador
            partes = linea.split(',')

            # Verificamos que tenga 4 elementos (PID, BT, AT, PRIORITY)
            if len(partes) == 4:
                pid = partes[0].strip()
                bt = partes[1].strip()
                at = partes[2].strip()
                priority = partes[3].strip()

                # Creamos un nuevo objeto Proceso
                nuevo_proceso = Proceso(pid, bt, at, priority)

                # Lo agregamos a la lista de procesos
                lista_procesos.append(nuevo_proceso)
            else:
                print("⚠️ Línea inválida (debe tener 4 elementos):", linea)

        # Cerramos el archivo después de usarlo
        archivo.close()

    except FileNotFoundError:
        print("❌ Error: El archivo no fue encontrado:", nombre_archivo)

    # Retornamos la lista de procesos creados
    return lista_procesos
