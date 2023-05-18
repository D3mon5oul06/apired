from pydantic import BaseModel

class UserCreate(BaseModel):
    nombre_usuario: str
    password: str
