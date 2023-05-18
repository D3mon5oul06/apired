from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import errorcode
from minio import Minio
import io


try:
    cnx = mysql.connector.connect(user='root',password="",database='alpr')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = cnx.cursor()
  
class Item(BaseModel):
    user: str
    passw: str 
    
app = FastAPI()

@app.post("/login")
def login(user,passw):
    statement = "Select tipo_usuario from users where nombre_usuario = %s and password = %s"
    cursor.execute(statement, (user, passw))
    print(cursor)
    cur=cursor.fetchone()
    if len(cur) == 0:
        return 0
    else:
        return cur[0]


class User(BaseModel):
    id_persona: str
    nombre_usuario: str
    password: str
    tipo: str
    tipo_usuario: str

@app.post("/users")
def create_user(user: User):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "INSERT INTO users (id_persona, nombre_usuario, password, tipo, tipo_usuario) " \
                    "VALUES (%s, %s, %s, %s, %s)"
        data = (user.id_persona, user.nombre_usuario, user.password, user.tipo, user.tipo_usuario)

        cursor.execute(statement, data)
        cnx.commit()

        return {"message": "User created successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "SELECT * FROM users WHERE id_persona = %s"
        data = (user_id,)

        cursor.execute(statement, data)
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        user = {
            "id_persona": result[0],
            "nombre_usuario": result[1],
            "password": result[2],
            "tipo": result[3],
            "tipo_usuario": result[4]
        }

        return user
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.put("/users/{user_id}")
def update_user(user_id: str, user_update: User):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "UPDATE users SET nombre_usuario = %s, password = %s, tipo = %s, tipo_usuario = %s " \
                    "WHERE id_persona = %s"
        data = (user_update.nombre_usuario, user_update.password, user_update.tipo,
                user_update.tipo_usuario, user_id)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User updated successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        cnx = mysql.connector.connect(user='root', password='', database='alpr')
        cursor = cnx.cursor()

        statement = "DELETE FROM users WHERE id_persona = %s"
        data = (user_id,)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}

#crud ine
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

#crud vehiculo
class Vehiculo(BaseModel):
    placa: str
    modelo: str
    color: str
    año: str
    marca: str
    vin: str
    num_puertas: int
    tipo_motor: str
try:
    cnx = mysql.connector.connect(user='root', password="", database='alpr')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = cnx.cursor()



@app.post("/vehiculos")
def create_vehiculo(vehiculo: Vehiculo):
    try:
        statement = "INSERT INTO vehiculo (placa, modelo, color, año, marca, vin, num_puertas, tipo_motor) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (vehiculo.placa, vehiculo.modelo, vehiculo.color, vehiculo.año, vehiculo.marca,
                vehiculo.vin, vehiculo.num_puertas, vehiculo.tipo_motor)

        cursor.execute(statement, data)
        cnx.commit()

        return {"message": "Vehiculo created successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.get("/vehiculos/{placa}")
def get_vehiculo(placa: str):
    try:
        statement = "SELECT * FROM vehiculo WHERE placa = %s"
        data = (placa,)

        cursor.execute(statement, data)
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Vehiculo not found")

        vehiculo = {
            "placa": result[0],
            "modelo": result[1],
            "color": result[2],
            "año": result[3],
            "marca": result[4],
            "vin": result[5],
            "num_puertas": result[6],
            "tipo_motor": result[7]
        }

        return vehiculo
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.put("/vehiculos/{placa}")
def update_vehiculo(placa: str, vehiculo_update: Vehiculo):
    try:
        statement = "UPDATE vehiculo SET modelo = %s, color = %s, año = %s, marca = %s, " \
                    "vin = %s, num_puertas = %s, tipo_motor = %s WHERE placa = %s"
        data = (vehiculo_update.modelo, vehiculo_update.color, vehiculo_update.año,
                vehiculo_update.marca, vehiculo_update.vin, vehiculo_update.num_puertas,
                vehiculo_update.tipo_motor, placa)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehiculo not found")

        return {"message": "Vehiculo updated successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.delete("/vehiculos/{placa}")
def delete_vehiculo(placa: str):
    try:
        statement = "DELETE FROM vehiculo WHERE placa = %s"
        data = (placa,)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehiculo not found")

        return {"message": "Vehiculo deleted successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
            
#crud persona
class Persona(BaseModel):
    curp: str
    nombre: str
    edad: int
    correo_electronico: str
    id_ine: str
    vin: str
try:
    cnx = mysql.connector.connect(user='root', password='', database='alpr')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


@app.post("/personas")
def create_persona(persona: Persona):
    try:
        statement = "INSERT INTO persona (curp, nombre, edad, correo_electronico, id_ine, vin) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
        data = (persona.curp, persona.nombre, persona.edad, persona.correo_electronico,
                persona.id_ine, persona.vin)

        cursor.execute(statement, data)
        cnx.commit()

        return {"message": "Persona created successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}

@app.get("/personas/{curp}")
def get_persona(curp: str):
    try:
        statement = "SELECT * FROM persona WHERE curp = %s"
        data = (curp,)

        cursor.execute(statement, data)
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Persona not found")

        persona = {
            "curp": result[0],
            "nombre": result[1],
            "edad": result[2],
            "correo_electronico": result[3],
            "id_ine": result[4],
            "vin": result[5]
        }

        return persona
    except mysql.connector.Error as err:
        return {"error": str(err)}

@app.put("/personas/{curp}")
def update_persona(curp: str, persona_update: Persona):
    try:
        statement = "UPDATE persona SET nombre = %s, edad = %s, correo_electronico = %s, " \
                    "id_ine = %s, vin = %s WHERE curp = %s"
        data = (persona_update.nombre, persona_update.edad, persona_update.correo_electronico,
                persona_update.id_ine, persona_update.vin, curp)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Persona not found")

        return {"message": "Persona updated successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}

@app.delete("/personas/{curp}")
def delete_persona(curp: str):
    try:
        statement = "DELETE FROM persona WHERE curp = %s"
        data = (curp,)

        cursor.execute(statement, data)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Persona not found")

        return {"message": "Persona deleted successfully"}
    except mysql.connector.Error as err:
        return {"error": str(err)}

