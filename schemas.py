"""
Esquemas para los monstruos en el juego de Dungeons & Dragons (DnD).
Estos esquemas definen la estructura de los datos para los monstruos, incluyendo sus atributos, iniciativa y ataque base.
Se utilizan para la validación de datos y la serialización/deserialización en la aplicación
"""

from pydantic import BaseModel

# ==========================================
# 🐉 ESQUEMAS PARA LOS MONSTRUOS
# ==========================================

#🛠️ Se crea el modelo de validación de los datos
class MonstruoBase(BaseModel):
    nombre_monstruo: str
    iniciativa : int = 0
    ataque_base : int = 0
    fuerza : int = 10
    destreza : int = 10
    constitucion : int = 10
    inteligencia : int = 10
    sabiduria : int = 10
    carisma : int = 10


# 🛠️ Se hereda el modelo para la creación de un monstruo
class MonstruoCreate(MonstruoBase):
    pass

# 🐉 Se hereda el modelo para la representación de un monstruo con su ID
class Monstruo(MonstruoBase):
    id: int

    #💡 Se agrega la configuración para permitir la creación de instancias a partir de atributos
    class Config:
        from_attributes = True






