# Se importa la función create_engine de SQLAlchemy, que se utiliza para crear un motor de base de datos
from sqlalchemy import create_engine

# Se importa la función declarative_base de SQLAlchemy, que se utiliza para crear una clase base para los modelos de la base de datos
from sqlalchemy.ext.declarative import declarative_base

# Se importa la función sessionmaker de SQLAlchemy, que se utiliza para crear una clase de sesión para interactuar con la base de datos
from sqlalchemy.orm import sessionmaker

# Datos de conexión a la base de datos PostgreSQL, incluyendo el nombre de usuario, contraseña, host, puerto y nombre de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:86667681@localhost:5432/tablero_dnd"

# Se crea el motor de la base de datos utilizando la URL proporcionada apuntando a la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Se configura la sesión de la base de datos, estableciendo que no se realicen commits automáticos ni flush automáticos, y vinculándola al motor creado
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Se define la base para los modelos de SQLAlchemy:
# sirve como clase base de la que deben heredar todos los modelos de datos para habilitar el mapeo automático entre clases Python y tablas de la base de datos
Base = declarative_base()

# Mensaje para indicar que la conexión a la base de datos se ha establecido correctamente
print("Conexión a la base de datos establecida correctamente.")
