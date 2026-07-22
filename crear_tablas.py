
from database import Base, engine

"""
Objetivo: Crear tablas en la base de datos PostgreSQL utilizando SQLAlchemy y el modelo definido en models.py.
Este script se encarga de crear las tablas en la base de datos según los modelos definidos en models.py.
Se utiliza SQLAlchemy para interactuar con la base de datos y crear las tablas correspondientes.

"""

# Mensaje para saber que empezó a trabajar
print("Construyendo la base de datos...")

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Mensaje para saber que terminó de trabajar
print("Base de datos construida correctamente")
