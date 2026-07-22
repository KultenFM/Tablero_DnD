
#📌 Importación de las clases y funciones necesarias de SQLAlchemy para definir modelos de base de datos
from database import Base
from sqlalchemy import Column, Integer, String


# Una clase representa una tabla en la base de datos y un objeto de esa clase representa una fila en la tabla.
#🛠️ Definición del modelo de datos para la tabla "monstruos" en la base de datos
class Monstruo(Base):
    # Nombre real de la tabla en PostgreSQL
    __tablename__ = "monstruos"

    # 🆔 Identificación
    id = Column(Integer, primary_key=True, index=True)
    nombre_monstruo = Column(String, index=True)

    # ⚔️ Estadísticas de Combate
    iniciativa = Column(Integer)
    ataque_base = Column(Integer)

    # 💪 Atributos
    fuerza = Column(Integer)
    destreza = Column(Integer)
    constitucion = Column(Integer)
    inteligencia = Column(Integer)
    sabiduria = Column(Integer)
    carisma = Column(Integer)
