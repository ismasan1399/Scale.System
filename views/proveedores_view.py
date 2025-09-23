from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from controllers.proveedores_controller import agregar_proveedor, obtener_proveedores, eliminar_proveedor

class ProveedoresView(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.form_layout = QHBoxLayout()
        self.layout().addLayout(self.form_layout)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección")
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo")
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono")

        for input_widget in (
            self.input_nombre,
            self.input_direccion,
            self.input_correo,
            self.input_telefono
        ):
            self.form_layout.addWidget(input_widget)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar proveedor")
        self.btn_agregar.clicked.connect(self.agregar_proveedor)
        botones_layout.addWidget(self.btn_agregar)

        self.btn_eliminar = QPushButton("Eliminar proveedor seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        botones_layout.addWidget(self.btn_eliminar)

        self.layout().addLayout(botones_layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Dirección", "Correo", "Teléfono"])
        
        # Ajustar columnas
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(1, QHeaderView.Stretch)  
        header.setSectionResizeMode(2, QHeaderView.Stretch)  
        header.setSectionResizeMode(3, QHeaderView.Stretch)  
        
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)    
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)    
        self.layout().addWidget(self.tabla)

        self.cargar_proveedores()

        self.setStyleSheet("""
        QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView::section {
            color: #2f3542;
            font-size: 14px;
        }
        QLineEdit {
            background-color: white;
            border: 1px solid #ced6e0;
            padding: 5px;
            border-radius: 4px;
        }
        QPushButton {
            background-color: #70a1ff;
            color: white;
            padding: 5px 10px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1e90ff;
        }
        QTableWidget {
            background-color: white;
            border: 1px solid #ced6e0;
        }
        """)

    def cargar_proveedores(self):
        self.tabla.setRowCount(0)
        proveedores = obtener_proveedores()
        for i, proveedor in enumerate(proveedores):
            self.tabla.insertRow(i)
            for j in range(5):
                self.tabla.setItem(i, j, QTableWidgetItem(str(proveedor[j])))

    def agregar_proveedor(self):
        nombre = self.input_nombre.text()
        direccion = self.input_direccion.text()
        correo = self.input_correo.text()
        telefono = self.input_telefono.text()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        agregar_proveedor(nombre, direccion, correo, telefono)
        QMessageBox.information(self, "Éxito", "Proveedor agregado")
        self.input_nombre.clear()
        self.input_direccion.clear()
        self.input_correo.clear()
        self.input_telefono.clear()
        self.cargar_proveedores()

    def eliminar_seleccionado(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un proveedor primero.")
            return

        id_item = self.tabla.item(fila, 0)
        if id_item:
            id_proveedor = int(id_item.text())
            confirm = QMessageBox.question(
                self,
                "Confirmar",
                f"¿Eliminar al proveedor con ID {id_proveedor}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                eliminar_proveedor(id_proveedor)
                QMessageBox.information(self, "Eliminado", "Proveedor eliminado con éxito.")
                self.cargar_proveedores()