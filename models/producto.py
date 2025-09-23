class Producto:
    def __init__(
        self,
        id_producto,
        nombre,
        descripcion,
        id_categoria,
        precio_base,
        id_proveedor=None,
        fecha_creacion=None,
        stock_total=None  
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_categoria = id_categoria
        self.precio_base = precio_base
        self.id_proveedor = id_proveedor
        self.fecha_creacion = fecha_creacion
        self.stock_total = stock_total  