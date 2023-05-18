from sqlalchemy import Column, Integer, String

import conexion

class User(conexion.engine):
    __tablename__ = "users"
    id_persona = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), index=True)
    password = Column(String(50))
    tipo = Column(Integer)
