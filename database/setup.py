import sqlite3

# 0 = False, 1 = True
# ISO format YYYY-MM-DD
# ISO datetime format YYYY-MM-DD HH:MM:SS
# este script fue utilizado para crear las tablas de la base de datos aqui pueden ver la estructura correpondiente para el desarrollo de los modulos.

def create_tables(conn):
    cursor = conn.cursor()

    # Tabla de categorías
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    )
    """)

    # Tabla de proveedores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        correo TEXT,
        telefono TEXT,
        fecha_registro TEXT  
    )
    """)

    # Tabla de productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        id_categoria INTEGER NOT NULL,
        precio_base REAL NOT NULL,
        id_proveedor INTEGER,
        fecha_creacion TEXT,  
        FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
        FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
    )
    """)

    # Tabla de variantes de producto
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS variantes_producto (
        id_variante INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER NOT NULL,
        talla TEXT,
        color TEXT,
        stock INTEGER DEFAULT 0,
        sku TEXT UNIQUE,
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
    )
    """)

    # Tabla de ofertas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ofertas (
        id_oferta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER NOT NULL,
        porcentaje_descuento REAL NOT NULL,
        fecha_inicio TEXT NOT NULL,  
        fecha_fin TEXT NOT NULL,     
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
    )
    """)

    # Tabla de clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        correo TEXT,
        telefono TEXT,
        fecha_registro TEXT 
    )
    """)

    # Tabla de ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        fecha_venta TEXT NOT NULL,  
        metodo_pago TEXT CHECK(metodo_pago IN ('EFECTIVO', 'TARJETA', 'TRANSFERENCIA')),
        total REAL NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
    )
    """)

    # Tabla de detalle de ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER NOT NULL,
        id_variante INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        descuento_aplicado REAL DEFAULT 0,
        FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
        FOREIGN KEY (id_variante) REFERENCES variantes_producto(id_variante)
    )
    """)

    conn.commit()
    print("Base de datos creada correctamente.")

def initialize_database(path="scale_system.db"):
    conn = sqlite3.connect(path)
    create_tables(conn)
    conn.close()

if __name__ == "__main__":
    initialize_database()
