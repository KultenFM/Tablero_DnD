
# 📌 Importación de librerias
import pandas as pd  # Libreria para manejar datos en forma de tablas (DataFrames)
import requests  # Libreria para hacer peticiones a la API y obtener datos de la misma
import streamlit as st  # Motor gráfico de la aplicación. st es una abreviación de streamlit

# 📌 1. Configuración de la página de la aplicación
st.set_page_config(
    page_title="Tablero D&D",
    page_icon="🐉",
    layout="wide",
)
# 📌 2. Título  principal de la aplicación
st.title("🧟‍♂️ Tablero de Control del Dungeon Master")

# 📌 3. Formulario: Entrada de datos del monstruo
# with sirve para agrupar elementos de la interfaz gráfica en un bloque, en este caso, un formulario para registrar monstruos.
with st.form("Formulario de Registro Monstruo"):
    nombre_monstruo = st.text_input("Nombre del Monstruo")
    tirada_iniciativa = st.number_input("Iniciativa", value=0)
    ataque_base = st.number_input("Ataque Base", value=0)
    atr_fuerza = st.number_input("Fuerza", value=10)
    atr_destreza = st.number_input("Destreza", value=10)
    atr_constitucion = st.number_input("Constitución", value=10)
    atr_inteligencia = st.number_input("Inteligencia", value=10)
    atr_sabiduria = st.number_input("Sabiduría", value=10)
    atr_carisma = st.number_input("Carisma", value=10)
    crear_boton = st.form_submit_button(label="Registrar Monstruo")

# 📌 4. Evaluamos si el botón del formulario fue precionado
if crear_boton:
    #▫️ 4.1 Creamos un diccionario con los datos del monstruo
    datos_monstruo = {
        "nombre": nombre_monstruo,
        "iniciativa": tirada_iniciativa,
        "ataque_base": ataque_base,
        "fuerza": atr_fuerza,
        "destreza": atr_destreza,
        "constitucion": atr_constitucion,
        "inteligencia": atr_inteligencia,
        "sabiduria": atr_sabiduria,
        "carisma": atr_carisma
    }
    #▫️ 4.2 Hacemos una petición POST a la API para registrar el monstruo en la base de datos
    # El json=datos_monstruo convierte el diccionario en un formato JSON que la API puede entender.
    response = requests.post("http://127.0.0.1:8000/monstruos/", json=datos_monstruo)

    #▫️ 4.3 Evaluamos la respuesta de la API
    # # 200 es el código de éxito HTTP estándar que indica que la solicitud se ha procesado correctamente. Si no, hubo un error.
    if response.status_code == 200:
        st.success("Monstruo registrado exitosamente")
    else:
        st.error("Error al registrar el monstruo")







