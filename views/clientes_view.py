from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente_data=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Cliente" if cliente_data is None else "Editar Cliente")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Formulario
        form = QFormLayout()
        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet("color: black;")
        self.input_correo = QLineEdit()
        self.input_correo.setStyleSheet("color: black;")
        self.input_telefono = QLineEdit()
        self.input_telefono.setStyleSheet("color: black;")
        self.input_direccion = QLineEdit()
        self.input_direccion.setStyleSheet("color: black;")
        
        form.addRow("Nombre:", self.input_nombre)
        form.addRow("Correo:", self.input_correo)
        form.addRow("Teléfono:", self.input_telefono)
        form.addRow("Dirección:", self.input_direccion)
        
        # Color negro a los labels del formulario
        for i in range(form.rowCount()):
            label = form.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setStyleSheet("color: black;")
        
        # Precargar datos si es edición
        if cliente_data:
            self.input_nombre.setText(cliente_data.get('nombre', ''))
            self.input_correo.setText(cliente_data.get('correo', ''))
            self.input_telefono.setText(cliente_data.get('telefono', ''))
            self.input_direccion.setText(cliente_data.get('direccion', ''))
        
        layout.addLayout(form)
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("color: black;")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def get_data(self):
        return {
            'nombre': self.input_nombre.text().strip(),
            'correo': self.input_correo.text().strip(),
            'telefono': self.input_telefono.text().strip(),
            'direccion': self.input_direccion.text().strip()
        }
    
    def validate_data(self):
        data = self.get_data()
        if not data['nombre']:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return False
        if not data['correo']:
            QMessageBox.warning(self, "Error", "El correo es obligatorio")
            return False
        return True

class ClientesView(QWidget):
    def __init__(self):
        super().__init__()
        self.clientes_data = []  # Lista para almacenar los datos de clientes
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("Gestión de Clientes")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout.addWidget(title)

        # Tabla para mostrar clientes
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Correo", "Teléfono", "Dirección", "Acciones"
        ])
        self.table.setStyleSheet("color: black;")
        self.table.horizontalHeader().setStyleSheet("color: black; font-weight: bold;")
        
        # Ajustar el ancho de las columnas
        header = self.table.horizontalHeader()
        header.setStyleSheet("color: black; font-weight: bold;")
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nombre
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Correo
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Dirección
        
        layout.addWidget(self.table)

        # Botón Agregar
        btn_agregar = QPushButton("Agregar Cliente")
        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_agregar.clicked.connect(self.agregar_cliente)
        layout.addWidget(btn_agregar)


    def actualizar_tabla(self):
        """Actualiza la tabla con los datos actuales"""
        self.table.setRowCount(len(self.clientes_data))
        
        for row, cliente in enumerate(self.clientes_data):
            # Datos del cliente
            self.table.setItem(row, 0, QTableWidgetItem(str(cliente["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(cliente["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(cliente["correo"]))
            self.table.setItem(row, 3, QTableWidgetItem(cliente["telefono"]))
            self.table.setItem(row, 4, QTableWidgetItem(cliente["direccion"]))
            
            # Botones de acción
            widget_acciones = QWidget()
            layout_acciones = QHBoxLayout(widget_acciones)
            layout_acciones.setContentsMargins(5, 5, 5, 5)
            
            # Botón Editar
            btn_editar = QPushButton("Editar")
            btn_editar.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            btn_editar.clicked.connect(lambda checked, r=row: self.editar_cliente(r))
            
            # Botón Eliminar
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
            btn_eliminar.clicked.connect(lambda checked, r=row: self.eliminar_cliente(r))
            
            layout_acciones.addWidget(btn_editar)
            layout_acciones.addWidget(btn_eliminar)
            
            self.table.setCellWidget(row, 5, widget_acciones)

    def agregar_cliente(self):
        """Abre el diálogo para agregar un nuevo cliente"""
        dialog = ClienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            if dialog.validate_data():
                data = dialog.get_data()
                # Generar nuevo ID
                nuevo_id = max([c["id"] for c in self.clientes_data], default=0) + 1
                data["id"] = nuevo_id
                self.clientes_data.append(data)
                self.actualizar_tabla()
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Cliente agregado correctamente")
                msg.setWindowTitle("Éxito")
                msg.setStyleSheet("color: black;")
                msg.exec_()

    def editar_cliente(self, row):
        """Abre el diálogo para editar un cliente existente"""
        if row < len(self.clientes_data):
            cliente_actual = self.clientes_data[row]
            dialog = ClienteDialog(self, cliente_actual)
            if dialog.exec_() == QDialog.Accepted:
                if dialog.validate_data():
                    data = dialog.get_data()
                    data["id"] = cliente_actual["id"]  # Mantener el ID original
                    self.clientes_data[row] = data
                    self.actualizar_tabla()
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Cliente actualizado correctamente")
                    msg.setWindowTitle("Éxito")
                    msg.setStyleSheet("color: black;")
                    msg.exec_()

    def eliminar_cliente(self, row):
        """Elimina un cliente después de confirmación"""
        if row < len(self.clientes_data):
            cliente = self.clientes_data[row]
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle("Confirmar eliminación")
            msg_box.setText(f"¿Está seguro de eliminar al cliente '{cliente['nombre']}'?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setStyleSheet("color: black;")
            respuesta = msg_box.exec_()
            if respuesta == QMessageBox.Yes:
                del self.clientes_data[row]
                self.actualizar_tabla()
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Cliente eliminado correctamente")
                msg.setWindowTitle("Éxito")
                msg.setStyleSheet("color: black;")
                msg.exec_()

    def mostrar_clientes(self, clientes):
        """Método para compatibilidad con código existente"""
        self.clientes_data = clientes
        self.actualizar_tabla()