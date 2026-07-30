"""
Módulo de búsqueda de monstruos para la aplicación de D&D
Este módulo proporciona una interfaz de Streamlit para buscar y visualizar información de monstruos desde una API REST.
"""
import pandas as pd
import requests
import streamlit as st

#📌1. Constantes
URL_API = "http://127.0.0.1:8000/monstruos/"
TIMEOUT_SEGUNDOS = 5

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 🛠️ Funcion 1: Obtener los monstruos de la API
def obtener_monstruos_desde_api():
    """
    Obtiene la lista de monstruos desde la API.
    Realiza una petición GET a la API de monstruos y maneja los posibles errores de conexión, timeout y respuestas HTTP.

    Returns:
        pd.DataFrame: DataFrame con los datos de monstruos.
            Retorna DataFrame vacío si hay error de conexión o si la API responde con código de error.
    """
    try:
        respuesta = requests.get(URL_API, timeout=TIMEOUT_SEGUNDOS)

        if respuesta.status_code == 200:
            monstruos_json = respuesta.json()
            return pd.DataFrame(monstruos_json)
        else:
            st.error(
                f"❌ Error en la API: Código {respuesta.status_code}"
            )
            return pd.DataFrame()

    # ‼️ Manejo de errores de conexión y timeout
    # requests.exceptions.ConnectionError: Error de conexión a la API
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ No se pudo conectar con la API. "
            "Verifica que el servidor esté ejecutándose en "
            "http://127.0.0.1:8000"
        )
        return pd.DataFrame()

    # requests.exceptions.Timeout: La API tardó demasiado en responder
    except requests.exceptions.Timeout:
        st.error(
            "⏱️ La API tardó demasiado en responder. "
            "Intenta nuevamente."
        )
        return pd.DataFrame()

    # requests.exceptions.RequestException: Otros errores de solicitud
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión: {e}")
        return pd.DataFrame()

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 🛠️ Funcion 2: Filtrar monstruos por nombre
def filtrar_monstruos(df, nombre_busqueda):
    """
    Filtra monstruos por nombre usando búsqueda parcial.
    Realiza una búsqueda case-insensitive del texto ingresado en la columna 'nombre' del DataFrame.

    Args:
        df (pd.DataFrame): DataFrame con los monstruos. nombre_busqueda (str): Texto de búsqueda parcial.

    Returns:
        pd.DataFrame: DataFrame filtrado con los monstruos que coinciden con la búsqueda.
    """
    return df[
        df['nombre'].str.contains(
            nombre_busqueda,
            case=False,
            na=False
        )
    ]

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 🛠️ Funcion 3: Mostrar resultados en la interfaz
def mostrar_resultados(df_filtrado, nombre_busqueda):
    """Muestra los resultados de búsqueda en la interfaz.

    Si hay resultados, muestra un mensaje de éxito y el DataFrame.
    Si no hay resultados, muestra advertencia y sugerencia.

    Args:
        df_filtrado (pd.DataFrame): DataFrame con resultados.
        nombre_busqueda (str): Texto de búsqueda del usuario.
    """
    if not df_filtrado.empty:
        # ST. Success y DataFrame para mostrar resultados
        st.success(
            f"✅ Se encontraron {len(df_filtrado)} monstruo(s)"
        )
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning(
            f"⚠️ No se encontraron monstruos con el nombre "
            f"'{nombre_busqueda}'"
        )
        st.info(
            "💡 Intenta con otro nombre o verifica la ortografía"
        )

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 🛠️ Función principal de la aplicación
def main():
    """
    Inicializa la interfaz de Streamlit, maneja la entrada del usuario,
    obtiene datos de la API y muestra los resultados filtrados.
    """
    # 📌 1. Encabezado de la página
    st.header("🔍 Buscar Monstruos")

    # 📌 2. Campo de búsqueda
    nombre_monstruo = st.text_input(
        "Nombre del Monstruo",
        placeholder="Ejemplo: Goblin, Dragon, Orco...",
        help="Escribe el nombre completo o parcial del monstruo"
    )

    # 📌 3. Obtener datos de la API con spinner
    with st.spinner("🔄 Cargando datos de monstruos..."):
        df_monstruos = obtener_monstruos_desde_api()

    # 📌4. Filtrado y visualización de resultados
    if not df_monstruos.empty:
        if nombre_monstruo:
            df_filtrado = filtrar_monstruos(
                df_monstruos,
                nombre_monstruo
            )
            mostrar_resultados(df_filtrado, nombre_monstruo)
        else:
            st.info(
                f"📊 Mostrando todos los monstruos "
                f"({len(df_monstruos)} en total)"
            )
            st.dataframe(
                df_monstruos,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning(
            "⚠️ No hay monstruos disponibles en la base de datos"
        )

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# 🛠️ Punto de entrada del script
if __name__ == "__main__":
    main()




