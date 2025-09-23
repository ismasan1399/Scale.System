class Proveedor:
    def __init__(self, id_proveedor, nombre, direccion=None, correo=None, telefono=None, fecha_registro=None):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono
        self.fecha_registro = fecha_registro