# Productos
GET_ALL_PRODUCTOS_WITH_STOCK = """
SELECT 
    p.id_producto, 
    p.nombre, 
    p.descripcion, 
    p.precio_base,               
    COALESCE(SUM(vp.stock), 0) AS stock_total, 
    pr.nombre AS proveedor,      
    c.nombre AS categoria        
FROM productos p
LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
LEFT JOIN variantes_producto vp ON p.id_producto = vp.id_producto
GROUP BY p.id_producto
ORDER BY p.id_producto ASC;
"""
GET_PRODUCTOS_CON_VARIANTES = """
SELECT 
    p.id_producto,
    p.nombre,
    p.descripcion,
    p.precio_base,
    pr.id_proveedor,
    pr.nombre AS proveedor_nombre,
    c.id_categoria,
    c.nombre AS categoria_nombre,
    vp.id_variante     AS id_variante,
    vp.talla,
    vp.color,
    vp.stock           AS stock_variante,
    vp.sku
FROM productos p
LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
LEFT JOIN variantes_producto vp ON p.id_producto = vp.id_producto
ORDER BY p.id_producto, vp.id_variante;
"""

GET_PRODUCTO_BY_ID="SELECT * FROM productos WHERE id_producto = ?"

INSERT_PRODUCTO = """
INSERT INTO productos (nombre, descripcion, precio_base, id_proveedor, id_categoria, fecha_creacion)
VALUES (?, ?, ?, ?, ?, ?);
"""
UPDATE_PRODUCTO = """
UPDATE productos 
SET nombre = ?, descripcion = ?, precio_base = ?, id_proveedor = ?, id_categoria = ?
WHERE id_producto = ?;
"""
DELETE_PRODUCTO = "DELETE FROM productos WHERE id_producto = ?"

# Variantes de Producto

GET_VARIANTES_BY_PRODUCTO = """
SELECT id_variante, id_producto, talla, color, stock, sku
FROM variantes_producto
WHERE id_producto = ?;
"""
GET_VARIANTE_BY_ID = """
SELECT id_variante, id_producto, talla, color, stock, sku  
FROM variantes_producto
WHERE id_variante = ?;
"""

INSERT_VARIENTE = """
INSERT INTO variantes_producto (id_producto, talla, color, stock, sku)
VALUES (?, ?, ?, ?, ?)""" 

UPDATE_VARIANTE = """
UPDATE variantes_producto
SET talla = ?, color = ?, stock = ?
WHERE id_variante = ?;
"""

DELETE_VARIANTE = """
DELETE FROM variantes_producto
WHERE id_variante = ?;
"""

# Ofertas
INSERT_OFERTA = """
INSERT INTO ofertas (id_producto, porcentaje_descuento, fecha_inicio, fecha_fin) 
VALUES (?, ?, ?, ?)
"""

UPDATE_OFERTA = """
UPDATE ofertas 
SET porcentaje_descuento = ?, fecha_inicio = ?, fecha_fin = ?
WHERE id_oferta = ?;
"""

DELETE_OFERTA = "DELETE FROM ofertas WHERE id_oferta = ?"

GET_OFERTA_BY_IDPRODUCTO="SELECT * FROM ofertas WHERE id_producto = ?"

# Proveedores

INSERT_PROVEEDOR = """
INSERT INTO proveedores (nombre, direccion, correo, telefono)
VALUES (?, ?, ?, ?);
"""
DELETE_PROVEEDOR = "DELETE FROM proveedores WHERE id_proveedor = ?"

GET_ALL_PROVEEDORES = "SELECT * FROM proveedores ORDER BY id_proveedor ASC;"

GET_PROVEEDORES="""
        SELECT id_proveedor, nombre, direccion, correo, telefono, fecha_registro
        FROM proveedores
        ORDER BY id_proveedor ASC
"""


# Categorías
GET_ALL_CATEGORIAS = "SELECT * FROM categorias ORDER BY id_categoria ASC;"


# Clientes
INSERT_CLIENTE = """
INSERT INTO clientes (nombre, direccion, correo, telefono, fecha_registro)
VALUES (?, ?, ?, ?, ?);
"""

DELETE_CLIENTE = """
DELETE FROM clientes
WHERE id_cliente = ?;
"""

UPDATE_CLIENTE = """
UPDATE clientes
SET nombre = ?, direccion = ?, correo = ?, telefono = ?, fecha_registro = ?
WHERE id_cliente = ?;
"""

GET_ALL_CLIENTES = """
SELECT id_cliente, nombre, direccion, correo, telefono, fecha_registro
FROM clientes;
"""

#ventas
# Proveedores

INSERT_VENTA = """
INSERT INTO ventas (id_cliente, fecha_venta, metodo_pago, total)
VALUES (?, ?, ?, ?);
"""


GET_VENTA = "SELECT * FROM ventas ORDER BY id_venta ASC;"