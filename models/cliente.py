class Cliente:
    def __init__(self, id_cliente, nombre, direccion=None, correo=None, telefono=None, fecha_registro=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono
        self.fecha_registro = fecha_registro