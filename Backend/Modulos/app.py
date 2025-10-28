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
        entrada = bd.insert_historial(usuario_id,espacio,hora_entrada)
        return entrada
    elif not espacio and conectado:
        return {"mensaje": "No hay espacios disponibles"}
    else:
        return {"mensaje": "[ERROR] No hay conexion a Arduino"}

def verificar_ocupacion(espacio, forzar_invalido=False):
    print(f"entrando verificar_ocupacion{espacio}, forzar {forzar_invalido}")
    sensores = leer_espacios()
    ocupado = sensores.get(espacio) == 0
    if ocupado and espacio in espacios_pendientes:
        espacios_pendientes.remove(espacio)
    elif not ocupado and forzar_invalido:
        print(f"condicion de invalidacion cumplida {espacio}")
        bd.cambiar_valido_historial(espacio)
        espacios_pendientes.discard(espacio)
    return {"ocupado": ocupado}

def obtener_estado_espacios():
    sensores = leer_espacios()
    return{
        "sensores": sensores,
        "pendientes": list(espacios_pendientes)
    }

def obtener_historial():
    historial =  bd.get_historial()
    return historial

def borrar_historial():
    bd.purgar_historial()