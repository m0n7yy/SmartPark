# app.py

from Backend.Modulos.asignador import esta_conectado,asignar_espacio, leer_espacios, espacios_pendientes
from Backend.BaseDatos import bd
from datetime import datetime

def registrar_acceso():
    usuario_id = 1  # Simulado
    espacio = asignar_espacio()
    conectado = esta_conectado()
    hora_entrada = datetime.now()
    if espacio and conectado:
        entrada = bd.insertHistorial(usuario_id,espacio,hora_entrada)
        return entrada
    elif not espacio and conectado:
        return {"mensaje": "No hay espacios disponibles"}
    else:
        return {"mensaje": "[ERROR] No hay conexion a Arduino"}

def verificar_ocupacion(espacio):
    sensores = leer_espacios()
    ocupado = sensores.get(espacio) == 0
    if ocupado and espacio in espacios_pendientes:
        espacios_pendientes.remove(espacio)
    return {"ocupado": ocupado}

def obtener_historial():
    historial =  bd.getHistorial()
    return historial

def borrar_historial():
    bd.purgarHistorial()