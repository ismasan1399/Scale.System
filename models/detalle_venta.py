class DetalleVenta:
    def __init__(self, id_detalle, id_venta, id_variante, cantidad, precio_unitario, descuento_aplicado=0):
        self.id_detalle = id_detalle
        self.id_venta = id_venta
        self.id_variante = id_variante
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.descuento_aplicado = descuento_aplicado