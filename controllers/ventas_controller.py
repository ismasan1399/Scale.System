from database.connection import DatabaseConnection

from database.queries import (
    INSERT_VENTA,
    GET_VENTA
)

#Agregar venta
def agregar_venta(id, fecha, metpago, total):
    db = DatabaseConnection()
    query = INSERT_VENTA
    db.execute(query, (id,fecha, metpago, total),commit=True)
    db.close()

#Obtener las ventas
def obtener_venta():
    db =DatabaseConnection()
    query =  GET_VENTA
    resultado=db.execute(query)
    ventas = resultado.fetchall() if resultado else []
    db.close()
    return ventas
