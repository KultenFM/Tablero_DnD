import pandas as pd  # Libreria para manejar datos en forma de tablas (DataFrames)
import requests  # Libreria para hacer peticiones a la API y obtener datos de la misma
import streamlit as st  # Motor gráfico de la aplicación. st es una abreviación de streamlit

# 📌 1. Encabezado de la página
st.header("🔍 Buscar Monstruos")

# 📌 2. Campo de búsqueda
nombre_monstruo = st.text_input(
    "Nombre del Monstruo",
    placeholder="Ejemplo: Goblin, Dragon, Orco...",
    help="Escribe el nombre completo o parcial del monstruo que deseas buscar"
)

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 📌 3. Direccion del Endpoint
URL_API = "http://127.0.0.1:8000/monstruos/"

# 📌 4. Petición a la API para obtener la lista de monstruos
# Usamos un spinner para indicar que se están cargando los datos
with st.spinner("🔄 Cargando datos de monstruos..."):
    try:
        respuesta = requests.get(URL_API, timeout=5) # Timeout de 5 segundos para evitar que la app se quede colgada

        if respuesta.status_code == 200:
            # Si la respuesta es exitosa, convertimos los datos JSON en un DataFrame de pandas
            monstruos_json = respuesta.json()
            df_monstruos = pd.DataFrame(monstruos_json)
        else:
            # si la API devuelve un código de error, mostramos un mensaje
            st.error(f"❌ Error en la API: Código {respuesta.status_code}")
            # Creamos un DataFrame vacío para evitar errores posteriores
            df_monstruos = pd.DataFrame()

    #‼️ Manejo de excepciones para errores de conexión y tiempo de espera
    # ConnectionError ocurre cuando no se puede establecer una conexión con la API
    except requests.exceptions.ConnectionError:
        st.error("❌ No se pudo conectar con la API. Verifica que el servidor esté ejecutándose en http://127.0.0.1:8000")
        df_monstruos = pd.DataFrame()

    # Timeout ocurre cuando la API tarda demasiado en responder
    except requests.exceptions.Timeout:
        st.error("⏱️ La API tardó demasiado en responder. Intenta nuevamente.")
        df_monstruos = pd.DataFrame()

    # RequestException captura cualquier otro error relacionado con la petición HTTP
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión: {(e)}")
        df_monstruos = pd.DataFrame()

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 📌 5. Filtrado y visualización de resultados
if not df_monstruos.empty:
    # Si el usuario escribió algo, filtramos
    if nombre_monstruo:
        # Filtrado insensible a mayúsculas y búsqueda parcial
        df_filtrado = df_monstruos[
            df_monstruos['nombre'].str.contains(nombre_monstruo, case=False, na=False)
        ]

        # Mostramos resultados
        if not df_filtrado.empty:
            st.success(f"✅ Se encontraron {len(df_filtrado)} monstruo(s)")
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning(f"⚠️ No se encontraron monstruos con el nombre '{nombre_monstruo}'")
            st.info("💡 Intenta con otro nombre o verifica la ortografía")
    else:
        # Si no hay búsqueda, mostramos todos con un mensaje
        st.info(f"📊 Mostrando todos los monstruos ({len(df_monstruos)} en total)")
        st.dataframe(
            df_monstruos,
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("⚠️ No hay monstruos disponibles en la base de datos")




