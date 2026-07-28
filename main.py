"""
Función de FastAPI: abrirá la conexión a la base de datos, usará los esquemas de Pydantic para validar
la entrada y usará los modelos de SQLAlchemy para guardar la información.
"""
# 📌 Importamos los módulos necesarios para la aplicacion FastAPI
import models
import schemas
from database import SessionLocal
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

# 🛠️  Creamos la aplicación FastAPI: Motor de la aplicación
app = FastAPI(title="API Tablero D&D - Dungeon Master")

# 🛠️ Funcion: Gestor que abre una sesión cada vez que llega una petición y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        # Yield permite que la función devuelva un valor y luego continúe ejecutándose después de que se haya usado ese valor.
        # En este caso, devuelve la sesión de la base de datos para que pueda ser utilizada en las rutas de FastAPI
        yield db
    finally:
        db.close()

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️
# ==========================================
# 📝 RUTAS DE LA API (ENDPOINTS)
# ==========================================

# ☝️ Definimos la ruta: POST para crear un nuevo monstruo
# response_model indica que la respuesta de esta ruta será del tipo Monstruo definido en schemas.py
# para asegurarnos de que la salida tenga el formato correcto
@app.post("/monstruos/", response_model=schemas.Monstruo)

# 🛠️ Función 1: Crear un monstruo por parte del usuario e insetarlo en la base de datos
def crear_monstruos(monstruo: schemas.MonstruoCreate, db: Session = Depends(get_db)):
    # 📌 Convertimos los datos validados de Pydantic a un objeto de SQLAlchemy (Traducción)
    nuevo_monstruo = models.Monstruo(**monstruo.model_dump())

    # 📌 Guardamos en la base de datos
    db.add(nuevo_monstruo)      # Agrega el nuevo monstruo a la sesión de la base de datos
    db.commit()                 # Guarda los cambios en la base de datos, lo que inserta el nuevo monstruo en la tabla correspondiente
    db.refresh(nuevo_monstruo)  # Actualiza el objeto nuevo_monstruo con los datos de la base de datos, incluyendo el ID generado automáticamente

    return nuevo_monstruo

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# ☝️ Definimos la ruta: GET para obtener la información de todos los monstruos del servidor
# response_model=list[schemas.Monstruo] indica que la respuesta de esta ruta será una lista de objetos del tipo Monstruo definido en schemas.py
@app.get("/monstruos/", response_model=list[schemas.Monstruo])

# 🛠️ Función 2: 🔍 Buscar todos los monstruos con el método GET en la base de datos
def buscar_monstruos(db: Session = Depends(get_db)):

    # 📌 1. Consultamos todos los monstruos directamente usando la sesión inyectada `db`
    lista_monstruos = db.query(models.Monstruo).all()

    # 📌 2. Se entrega la información al visitante
    return lista_monstruos

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

