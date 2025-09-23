from database.connection import DatabaseConnection

from database.queries import (
    INSERT_PROVEEDOR,
    DELETE_PROVEEDOR,
    GET_PROVEEDORES
)

#Agregar proveedor
def agregar_proveedor(nombre, direccion, correo, telefono):
    db = DatabaseConnection()
    query = INSERT_PROVEEDOR
    db.execute(query, (nombre,direccion, correo, telefono),commit=True)
    db.close()

#Obtener los proveedores
def obtener_proveedores():
    db =DatabaseConnection()
    query =  GET_PROVEEDORES
    resultado=db.execute(query)
    proveedores = resultado.fetchall() if resultado else []
    db.close()
    return proveedores

#Eliminar proveedor
def eliminar_proveedor(id_proveedor):
    db=DatabaseConnection()
    query = DELETE_PROVEEDOR
    db.execute(query,(id_proveedor,), commit=True)
    db.close()