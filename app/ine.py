from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

class User(BaseModel):
    id_persona: str
    nombre_usuario: str
    password: str
    tipo: str
    tipo_usuario: str

class INE(BaseModel):
    id_persona: str
    nombre: str
    curp: str
    fecha_nacimiento: str
    vigencia: str
    sexo: str
    foto: str
    domicilio: str
    clave_elector: str
    seccion: str
    localidad: str
    año_registro: int
    
@app.post("/login")
def login(user,passw):
    # Código para verificar usuarios en la tabla "users"
    pass

@app.post("/users")
def create_user(user: User):
    # Código para crear usuarios en la tabla "users"
    pass

@app.get("/users/{user_id}")
def get_user(user_id: str):
    # Código para obtener un usuario de la tabla "users"
    pass

@app.put("/users/{user_id}")
def update_user(user_id: str, user_update: User):
    # Código para actualizar un usuario en la tabla "users"
    pass

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    # Código para eliminar un usuario de la tabla "users"
    pass

@app.post("/ine")
def create_ine(ine: INE):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "INSERT INTO ine (id_persona, nombre, curp, fecha_nacimiento, vigencia, sexo, foto, " \
                    "domicilio, clave_elector, seccion, localidad, año_registro) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (ine.id_persona, ine.nombre, ine.curp, ine.fecha_nacimiento, ine.vigencia, ine.sexo,
                ine.foto, ine.domicilio, ine.clave_elector, ine.seccion, ine.localidad, ine.año_registro)

        cursor.execute(statement, data)
        cnx.commit()

        return {"message": "INE data created successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.get("/ine/{user_id}")
def get_ine(user_id: str):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "SELECT * FROM ine WHERE id_persona = %s"
        data = (user_id,)

        cursor.execute(statement, data)
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="INE data not found")

        ine_data = INE(id_persona=result[0], nombre=result[1], curp=result[2], fecha_nacimiento=result[3],
                       vigencia=result[4], sexo=result[5], foto=result[6], domicilio=result[7],
                       clave_elector=result[8], seccion=result[9], localidad=result[10], año_registro=result[11])
        
        return ine_data
    except mysql.connector.Error as err:
        return {"error": str(err)}

@app.put("/ine/{user_id}")
def update_ine(user_id: str, ine_update: INE):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "UPDATE ine SET nombre = %s, curp = %s, fecha_nacimiento = %s, vigencia = %s, " \
                    "sexo = %s, foto = %s, domicilio = %s, clave_elector = %s, seccion = %s, " \
                    "localidad = %s, año_registro = %s WHERE id_persona = %s"
        data = (ine_update.nombre, ine_update.curp, ine_update.fecha_nacimiento, ine_update.vigencia,
                ine_update.sexo, ine_update.foto, ine_update.domicilio, ine_update.clave_elector,
                ine_update.seccion, ine_update.localidad, ine_update.año_registro, user_id)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="INE data not found")

        return {"message": "INE data updated successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.delete("/ine/{user_id}")
def delete_ine(user_id: str):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "DELETE FROM ine WHERE id_persona = %s"
        data = (user_id,)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="INE data not found")

        return {"message": "INE data deleted successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()