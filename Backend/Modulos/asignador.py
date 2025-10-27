# asignador.py

import heapq
import time
import serial

etiquetas = ['A', 'B', 'C']
grafo = {
    'Entrada': {'A': 1},
    'A': {'C': 3},
    'B': {'A': 3},
    'C': {}
}
espacios_pendientes = set()

MESSAGE = "[ERROR] No hay conexion a Arduino"

#NOTA: Esta parte de código se debe adaptar para conexion wireless "POR VER"
# Inicializa Arduino solo una vez
try:
    arduino = serial.Serial('COM10', 9600)
    time.sleep(2)
    arduino.reset_input_buffer()
#Depuracion de conexion serial
except serial.SerialException as e:
    print(f"[ERROR] No se pudo abrir el puerto COM10: {e}")
    arduino = None

#Funcion anticrash
def esta_conectado():
    return arduino is not None and arduino.is_open    
#-------------------------------------------------------------------

#Por medio de arduino, lee los sensores activos y no activos
def leer_espacios(reintentos=10):
    if not esta_conectado:
        print(MESSAGE)
        return {}
    espacios = {}
    ultima_valida = None
    for _ in range(reintentos):
        if arduino:
            arduino.write(b'R')  # Solicita lectura
        linea = arduino.readline().decode().strip()
        print(f"[DEBUG] Línea recibida: {linea}")
        if not linea or "Asignado" in linea: #Lee que arduino este haciendo e/s
            continue
        valores = linea.split(',')
        if len(valores) != len(etiquetas):
            continue
        #Intenta dar los valores temporales para recibir siguientes peticiones
        try:
            temporal = {etiquetas[i]: int(valores[i]) for i in range(len(etiquetas))}
            ultima_valida = temporal
        except ValueError:
            continue
    return ultima_valida if ultima_valida else {}

#Algoritmo para asignar el espacio mas corto del grafo
def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola = [(0, inicio)]
    visitados = set()
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        for vecino, peso in grafo[nodo_actual].items():
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                heapq.heappush(cola, (nueva_distancia, vecino))
    return distancias

#Busca que el espacio este libre en los sensores y en la lista temporal
def encontrar_espacio_libre(distancias, sensores):
    libres = [espacio for espacio, estado in sensores.items() if estado == 1
              and espacio not in espacios_pendientes]
    if not libres:
        return None
    return min(libres, key=lambda x: distancias.get(x, float('inf')))

#Toma un tiempo para leer que el espacio este ocupado
def esperar_ocupacion(espacio_objetivo):
    while True:
        sensores = leer_espacios()
        if sensores.get(espacio_objetivo) == 0:
            return True
        time.sleep(1)

#Toma un tiempo para leer que el espacio este desocupado
def esperar_desocupacion(espacio_objetivo):
    sensores = leer_espacios()
    if sensores.get(espacio_objetivo) == 1:
        return
    while True:
        sensores = leer_espacios()
        if sensores.get(espacio_objetivo) == 1:
            return
        time.sleep(0.2)

#Funcion principal que realiza todo el proceso
def asignar_espacio():
    if not esta_conectado():
        print(f"[ERROR] No se puede asignar espacio: {MESSAGE}")
        return None
    sensores = leer_espacios()
    if not sensores:
        print(f"[ERROR] No se pudieron leer sensores {MESSAGE}")
        return None
    distancias = dijkstra(grafo, 'Entrada')
    espacio_objetivo = encontrar_espacio_libre(distancias, sensores)

    if espacio_objetivo:
        arduino.write(espacio_objetivo.encode())
        espacios_pendientes.add(espacio_objetivo)
        print(f"Espacio pendiente: {espacios_pendientes}")
        print(f"Asignado: {espacio_objetivo}")
        return espacio_objetivo
    return None
