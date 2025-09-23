import sqlite3
from PySide6.QtWidgets import QMessageBox

class ClientesController:
    def __init__(self, view):
        self.view = view
        self.view.set_controller(self)
        
        # Conectar los botones a los métodos del controlador
        self.view.btn_agregar.clicked.connect(self.agregar_cliente)
        self.view.btn_eliminar.clicked.connect(self.eliminar_cliente)
        self.view.btn_editar.clicked.connect(self.editar_cliente)
        
        # Cargar todos los clientes al inicializar
        self.mostrar_todos_los_clientes()

    def agregar_cliente(self):
        nombre = self.view.input_nombre.text()
        direccion = self.view.input_direccion.text()
        correo = self.view.input_correo.text()
        telefono = self.view.input_telefono.text()
        fecha_registro = self.view.input_fecha_registro.text()

        if not nombre:
            QMessageBox.warning(self.view, "Error", "El nombre es obligatorio.")
            return

        try:
            conn = sqlite3.connect("scale_system.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, direccion, correo, telefono, fecha_registro)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, direccion, correo, telefono, fecha_registro))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self.view, "Éxito", "Cliente agregado correctamente.")
            self.view.clear_inputs()
            self.mostrar_todos_los_clientes()
            
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Error al agregar cliente: {e}")

    def eliminar_cliente(self):
        id_cliente = self.view.input_id_cliente.text()
        if not id_cliente:
            QMessageBox.warning(self.view, "Error", "Debe seleccionar un cliente de la tabla para eliminar.")
            return

        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self.view, "Confirmar", f"¿Está seguro de eliminar el cliente con ID {id_cliente}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect("scale_system.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
                
                if cursor.rowcount == 0:
                    QMessageBox.warning(self.view, "Aviso", "No se encontró el cliente.")
                else:
                    conn.commit()
                    QMessageBox.information(self.view, "Éxito", "Cliente eliminado correctamente.")
                    self.view.clear_inputs()
                    self.mostrar_todos_los_clientes()
                    
                conn.close()
                
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Error al eliminar cliente: {e}")

    def editar_cliente(self):
        id_cliente = self.view.input_id_cliente.text()
        nombre = self.view.input_nombre.text()
        direccion = self.view.input_direccion.text()
        correo = self.view.input_correo.text()
        telefono = self.view.input_telefono.text()
        fecha_registro = self.view.input_fecha_registro.text()

        if not id_cliente or not nombre:
            QMessageBox.warning(self.view, "Error", "Debe seleccionar un cliente de la tabla y el nombre es obligatorio.")
            return

        try:
            conn = sqlite3.connect("scale_system.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nombre = ?, direccion = ?, correo = ?, telefono = ?, fecha_registro = ?
                WHERE id_cliente = ?
            """, (nombre, direccion, correo, telefono, fecha_registro, id_cliente))
            
            if cursor.rowcount == 0:
                QMessageBox.warning(self.view, "Aviso", "No se encontró el cliente.")
            else:
                conn.commit()
                QMessageBox.information(self.view, "Éxito", "Cliente editado correctamente.")
                self.view.clear_inputs()
                self.mostrar_todos_los_clientes()
                
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Error al editar cliente: {e}")

    def obtener_clientes(self):
        try:
            conn = sqlite3.connect("scale_system.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente, nombre, direccion, correo, telefono, fecha_registro FROM clientes")
            clientes = cursor.fetchall()
            conn.close()
            return clientes
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Error al obtener clientes: {e}")
            return []

    def mostrar_todos_los_clientes(self):
        clientes = self.obtener_clientes()
        self.view.mostrar_clientes(clientes)