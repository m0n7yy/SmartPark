# logica.py
from Backend.Modulos import app
from Backend.BaseDatos import bd

espacio_actual = [None]  # mutable para mantener estado

#def registrar(resultado, historial_texto, ventana):
def registrar(resultado, ventana):    
    datos = app.registrar_acceso()
    if "espacio_asignado" in datos:
        espacio_actual[0] = datos["espacio_asignado"]
        resultado.set(f"Usuario {datos['usuario_id']} → Espacio {datos['espacio_asignado']} @ {datos['hora_entrada']}")
        iniciar_verificacion_automatica(resultado, ventana)
    else:
        resultado.set(datos["mensaje"])
        return False

def iniciar_verificacion_automatica(resultado,ventana):
    if not espacio_actual[0]:
        return
    intentos = [0]

    def verificar_periodicamente():
        print("Ejecutando verificacion logica.py")
        estado = app.verificar_ocupacion(espacio_actual[0])
        if estado["ocupado"]:
            resultado.set(f"Espacio {espacio_actual[0]} ocupado")
        else:
            intentos[0] += 1
            print(f"Intento {intentos[0]} - espacio {espacio_actual[0]}")
            if intentos[0] >= 10:
                print(f"limite de intentos alcanzado")
                resultado.set(f"Espacio {espacio_actual[0]} no ocupado aún")
                app.verificar_ocupacion(espacio_actual[0],forzar_invalido=True)
                return
            ventana.after(2000, verificar_periodicamente)

    verificar_periodicamente()

def actualizar_visual(estado_botones):
    estado = app.obtener_estado_espacios()
    sensores = estado["sensores"]
    pendientes = estado["pendientes"]

    for etiqueta, boton in estado_botones.items():
        if etiqueta in pendientes:
            color = "yellow"
        elif sensores.get(etiqueta) == 0:
            color = "red"
        elif sensores.get(etiqueta) == 1:
            color = "green"
        else:
            color = "gray"
        boton.config(bg=color)

def mostrar_historial(historial_texto):
    historial = app.obtener_historial()
    texto = "\n".join([f"{h['historial_id']}| Usuario {h['usuario_id']} → {h['espacio_asignado']} @ {h['hora_entrada']} => {h['valido']}" for h in historial])
    historial_texto.set(texto)
    return historial_texto

def borrar_historial():
    app.borrar_historial()