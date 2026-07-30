"""
Función de FastAPI: abrirá la conexión a la base de datos, usará los esquemas de Pydantic para validar
la entrada y usará los modelos de SQLAlchemy para guardar la información.
"""
# 📌 Importamos los módulos necesarios para la aplicacion FastAPI
import models
import schemas
from database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException

# Importamos JSONResponse para personalizar las respuestas HTTP
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# 📌  Creamos la aplicación FastAPI: Motor de la aplicación
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

# ☝️ Definimos la ruta POST para crear un nuevo monstruo
# response_model indica que la respuesta de esta ruta será del tipo Monstruo definido en schemas.py
# para asegurarnos de que la salida tenga el formato correcto
@app.post("/monstruos/", response_model=schemas.Monstruo)

# 🛠️ Función 1: Crear un monstruo por parte del usuario e insetarlo en la base de datos
def crear_monstruos(monstruo: schemas.MonstruoCreate, db: Session = Depends(get_db)):
    #▫️1.1 Convertimos los datos validados de Pydantic a un objeto de SQLAlchemy (Traducción)
    nuevo_monstruo = models.Monstruo(**monstruo.model_dump())

    #▫️1.2 Guardamos en la base de datos
    db.add(nuevo_monstruo)      # Agrega el nuevo monstruo a la sesión de la base de datos
    db.commit()                 # Guarda los cambios en la base de datos, lo que inserta el nuevo monstruo en la tabla correspondiente
    db.refresh(nuevo_monstruo)  # Actualiza el objeto nuevo_monstruo con los datos de la base de datos, incluyendo el ID generado automáticamente

    return nuevo_monstruo

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# ☝️ Definimos la ruta GET para obtener la información de todos los monstruos del servidor
# response_model=list[schemas.Monstruo] indica que la respuesta de esta ruta será una lista de objetos del tipo Monstruo definido en schemas.py
@app.get("/monstruos/", response_model=list[schemas.Monstruo])

# 🛠️ Función 2: 🔍 Buscar todos los monstruos con el método GET en la base de datos
def buscar_monstruos(db: Session = Depends(get_db)):

    #▫️2.1. Consultamos todos los monstruos directamente usando la sesión inyectada `db`
    lista_monstruos = db.query(models.Monstruo).all()

    #▫️2.2 Se entrega la información al visitante
    return lista_monstruos

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# ☝️ Definimos la PUT para actualizar un monstruo existente en la base de datos
@app.put("/monstruos/{monstruo_id}", response_model=schemas.Monstruo)

# 🛠️ Función 3: Actualizar un monstruo existente en la base de datos
def actualizar_monstruo(monstruo_id: int, monstruo_actualizado: schemas.MonstruoCreate, db: Session = Depends(get_db)):

    #▫️3.1 Buscamos si el monstruo existe en la base de datos
    # Query: db.query(models.Monstruo) -> Selecciona la tabla Monstruo
    # Filter: .filter(models.Monstruo.id == monstruo_id) -> Filtra por el ID del monstruo que queremos actualizar
    # First: .first() -> Devuelve el primer resultado de la consulta o None si no existe
    db_monstruo = db.query(models.Monstruo).filter(models.Monstruo.id == monstruo_id).first()
    if db_monstruo is None:
        # Si no existe, lanzamos un error 404 controlado
        raise HTTPException(status_code=404, detail="¡El monstruo no existe o ha escapado!")

    #▫️3.2 Reemplazamos los valores viejos por los nuevos
    # setattr: es una función de Python que permite establecer el valor de un atributo de un objeto de manera dinámica.
    # En este caso, se usa para actualizar los atributos del objeto db_monstruo con los valores del objeto monstruo_actualizado.
    for clave, valor in monstruo_actualizado.model_dump().items():
        setattr(db_monstruo, clave, valor)

    #▫️3.3 Consolidamos los cambios en PostgreSQL
    db.commit()
    db.refresh(db_monstruo)
    return db_monstruo

# ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️

# ☝️ Definimos la DELETE para eliminar un monstruo existente en la base de datos
@app.delete("/monstruos/{monstruo_id}")

# 🛠️ Función 4: Eliminar un monstruo por su ID
def eliminar_monstruo(monstruo_id: int, db: Session = Depends(get_db)):

    #▫️4.1 Buscamos si el monstruo existe en la base de datos
    db_monstruo = db.query(models.Monstruo).filter(models.Monstruo.id == monstruo_id).first()
    if db_monstruo is None:
        # Si no existe, lanzamos un error 404 controlado
        raise HTTPException(status_code=404, detail="¡El monstruo no existe o ha escapado!")

    #▫️4.2 Si existe, lo borramos de la sesión y confirmamos a la base de datos
    db.delete(db_monstruo)
    db.commit()

    #▫️4.3 Mensaje de éxito en formato JSON
    # JSONResponse permite personalizar la respuesta HTTP, incluyendo el código de estado y el contenido)
    return JSONResponse(
        status_code=200,
        content={"message": f"El monstruo '{db_monstruo.nombre_monstruo}' ha sido eliminado con éxito de la base de datos."}
        )
