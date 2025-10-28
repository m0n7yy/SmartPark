import sqlite3 as sql
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR,"crud.db")

def conectar():
    conexion = sql.connect(DB_PATH)
    return conexion

def insert_historial(id_usuario,esp_asig,fecha_his):
    try:
        conexion = conectar()
    except sql.DatabaseError as e:
        print(f"Error en la base de datos {e}")
    cursor = conexion.cursor()
    sql = "INSERT INTO historial (idUsuario,espAsig,fechaHis) VALUES (?,?,?)"
    datos = (id_usuario,esp_asig,fecha_his)
    cursor.execute(sql,datos)
    conexion.commit()
    cursor.execute("SELECT idUsuario,espAsig,fechaHis,valido FROM historial ORDER BY idHis DESC LIMIT 1")
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexion.close()
        return{
            "usuario_id" : id_usuario,
            "espacio_asignado": esp_asig,
            "hora_entrada": fecha_his.strftime("%H:%M:%S"),
        }
    return {
        "usuario_id" : resultado[0],
        "espacio_asignado" : resultado[1],
        "hora_entrada" : resultado[2],
    }

def cambiar_valido_historial(espacio):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE historial SET valido = 0 WHERE idHis = (SELECT idHis FROM historial WHERE espAsig = ? AND valido = 1 ORDER BY idHis DESC LIMIT 1)"
    cursor.execute(sql,(espacio))
    conexion.commit()
    conexion.close()
    print(f"marcando como invalido {espacio}")

def get_historial():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT idHis, idUsuario, espAsig, fechaHis, valido from historial ORDER BY idHis DESC LIMIT 10")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    historial = []
    for fila in resultados:
        historial.append({
            "historial_id" : fila[0],
            "usuario_id" : fila[1],
            "espacio_asignado": fila[2],
            "hora_entrada" : fila[3],
            "valido": fila[4]
        })
    return historial

def purgar_historial():
    fecha_limite = (datetime.now() - timedelta(days=2)).date()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM historial WHERE fechaHis < ?", (fecha_limite,))
    conexion.commit()
    conexion.close()