from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import errorcode

app = FastAPI()

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

class Persona(BaseModel):
    curp: str
    nombre: str
    edad: int
    correo_electronico: str
    id_ine: str
    vin: str

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
