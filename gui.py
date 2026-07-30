
# 📌 Importación de librerias
import pandas as pd  # Libreria para manejar datos en forma de tablas (DataFrames)
import requests  # Libreria para hacer peticiones a la API y obtener datos de la misma
import streamlit as st  # Motor gráfico de la aplicación. st es una abreviación de streamlit

# 📌 1. Configuración de Metadatos de la página de la aplicación
st.set_page_config(
    page_title="Tablero D&D",
    page_icon="🐉",
    layout="wide",
)

# 📌 2. Título  principal de la aplicación
st.title("🧙‍♂️ Tablero de Control del Dungeon Master")

# 📌 3. Definir las páginas de la barra lateral con nombres
pagina_1 = st.Page("pages/buscar.py", title="🔍 Buscar")
pagina_2 = st.Page("pages/crear.py", title="➕ Crear")
pagina_3 = st.Page("pages/actualizar.py", title="✏️ Actualizar")
pagina_4 = st.Page("pages/eliminar.py", title="🗑️ Eliminar")

# 📌 4. Configurar la navegación en la barra lateral con título de sección
pg = st.navigation({
    "🧟‍♂️ Menú de Monstruos": [pagina_1, pagina_2, pagina_3, pagina_4]
})

# 📌 5. Ejecutar la página seleccionada
pg.run()











