class VarianteProducto:
    def __init__(self, id_variante, id_producto, talla, color, stock=0, sku=None):
        self.id_variante = id_variante
        self.id_producto = id_producto
        self.talla = talla
        self.color = color
        self.stock = stock
        self.sku = sku
