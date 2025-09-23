class Venta:
    def __init__(self, id_venta, id_cliente, fecha_venta, metodo_pago, total):
        self.id_venta = id_venta
        self.id_cliente = id_cliente
        self.fecha_venta = fecha_venta
        self.metodo_pago = metodo_pago
        self.total = total