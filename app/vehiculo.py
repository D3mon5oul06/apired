from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import errorcode

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

class Vehiculo(BaseModel):
    placa: str
    modelo: str
    color: str
    año: str
    marca: str
    vin: str
    num_puertas: int
    tipo_motor: str

app = FastAPI()

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