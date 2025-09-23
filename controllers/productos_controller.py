from database.connection import DatabaseConnection
from database.queries import (
    GET_ALL_PRODUCTOS_WITH_STOCK,
    GET_PRODUCTOS_CON_VARIANTES,
    GET_PRODUCTO_BY_ID,
    INSERT_PRODUCTO,
    UPDATE_PRODUCTO,
    DELETE_PRODUCTO,
    GET_VARIANTES_BY_PRODUCTO,
    GET_VARIANTE_BY_ID,
    GET_OFERTA_BY_IDPRODUCTO,
    INSERT_OFERTA,
    UPDATE_OFERTA,
    DELETE_OFERTA,
    INSERT_VARIENTE,
    UPDATE_VARIANTE,
    DELETE_VARIANTE,
    GET_ALL_PROVEEDORES,
    GET_ALL_CATEGORIAS
    
)
from models.producto import Producto
from models.variante_producto import VarianteProducto
from models.proveedor import Proveedor
from models.categoria import Categoria
from models.oferta import Oferta
from datetime import datetime

class ProductosController:
    def obtener_productos_con_stock(self):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_ALL_PRODUCTOS_WITH_STOCK)
        productos = cursor.fetchall() if cursor else []
        db.close()
        return productos
    
    def obtener_productos_con_variantes(self):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_PRODUCTOS_CON_VARIANTES)
        filas = cursor.fetchall() if cursor else []
        db.close()

        productos_map = {}
        for (
            id_p, nombre, desc, precio_base,
            id_prov, nombre_prov,
            id_cat, nombre_cat,
            id_var, talla, color, stock_var, sku
        ) in filas:
            if id_p not in productos_map:
                p = Producto(
                    id_producto=id_p,
                    nombre=nombre,
                    descripcion=desc,
                    id_categoria=id_cat,
                    precio_base=precio_base,
                    id_proveedor=id_prov,
                    fecha_creacion=None,
                    stock_total=None
                )
                p.proveedor_nombre = nombre_prov
                p.categoria_nombre = nombre_cat
                p.variantes = []
                productos_map[id_p] = p

            if id_var is not None:
                var = VarianteProducto(
                    id_variante=id_var,
                    id_producto=id_p,
                    talla=talla,
                    color=color,
                    stock=stock_var,
                    sku=sku
                )
                productos_map[id_p].variantes.append(var)

        return list(productos_map.values())
    
    def obtener_producto(self, id_producto):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_PRODUCTO_BY_ID, (id_producto,))
        fila = cursor.fetchone() if cursor else None
        db.close()
        return Producto(*fila) if fila else None
    
    def agregar_producto(self, nombre, descripcion, precio_base, id_proveedor, id_categoria):
        fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(INSERT_PRODUCTO, (nombre, descripcion, precio_base, id_proveedor, id_categoria, fecha_creacion), commit=True)
        producto_id = cursor.lastrowid if cursor else None
        db.close()
        return Producto(producto_id, nombre, descripcion, precio_base, id_proveedor, id_categoria)
    
    def editar_producto(self, id_producto, nombre, descripcion, precio_base, id_proveedor, id_categoria):
        db = DatabaseConnection()
        db.connect()
        db.execute(UPDATE_PRODUCTO, (nombre, descripcion, precio_base, id_proveedor, id_categoria,id_producto), commit=True)
        db.close()
        
    def eliminar_producto(self, id_producto):
        db = DatabaseConnection()
        db.connect()
        db.execute(DELETE_PRODUCTO, (id_producto,), commit=True)
        db.close()
    
    def obtener_variantes(self, producto_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_VARIANTES_BY_PRODUCTO, (producto_id,))
        filas = cursor.fetchall() if cursor else []
        db.close()
        return [VarianteProducto(*fila) for fila in filas]

    def agregar_variante(self, producto_id, talla, color, stock):
        # Generar un SKU único basado en el producto, talla y color
        sku = f"{producto_id}-{talla[:3].upper()}-{color[:3].upper()}"
        db = DatabaseConnection()
        db.connect()
        db.execute(INSERT_VARIENTE, (producto_id, talla, color, stock, sku), commit=True)
        db.close()

    def editar_variante(self, id_variante, talla, color, stock):
        db = DatabaseConnection()
        db.connect()
        db.execute(UPDATE_VARIANTE, (talla, color, stock, id_variante), commit=True)
        db.close()

    def eliminar_variante(self, id_variante):
        db = DatabaseConnection()
        db.connect()
        db.execute(DELETE_VARIANTE, (id_variante,), commit=True)
        db.close()
    
    def obtener_variante(self, id_variante):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_VARIANTE_BY_ID, (id_variante,))
        fila = cursor.fetchone() if cursor else None
        db.close()
        return VarianteProducto(*fila) if fila else None
    
    def obtener_proveedores(self):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_ALL_PROVEEDORES)
        proveedores = cursor.fetchall() if cursor else []
        db.close()
        return [Proveedor(*fila) for fila in proveedores]
    
    def obtener_categorias(self):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_ALL_CATEGORIAS)
        categorias = cursor.fetchall() if cursor else []
        db.close()
        return [Categoria(*fila) for fila in categorias]
    
    def obtener_oferta_por_producto(self, id_producto):
        db = DatabaseConnection()
        db.connect()
        cursor = db.execute(GET_OFERTA_BY_IDPRODUCTO, (id_producto,))
        row = cursor.fetchone()
        db.close()
        return Oferta(*row) if row else None

    def agregar_oferta(self, id_producto, porcentaje, fecha_inicio, fecha_fin):
        db = DatabaseConnection()
        db.connect()
        db.execute(INSERT_OFERTA,(id_producto, porcentaje, fecha_inicio, fecha_fin),commit=True)
        db.close()

    def actualizar_oferta(self, id_oferta, porcentaje, fecha_inicio, fecha_fin):
        db = DatabaseConnection()
        db.connect()
        db.execute(UPDATE_OFERTA,(porcentaje, fecha_inicio, fecha_fin, id_oferta),commit=True)
        db.close()

    def eliminar_oferta(self, id_oferta):
        db = DatabaseConnection()
        db.connect()
        db.execute(DELETE_OFERTA, (id_oferta,), commit=True)
        db.close()