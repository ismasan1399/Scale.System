from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from controllers.ventas_controller import agregar_venta, obtener_venta

class VentaView(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.form_layout = QHBoxLayout()
        self.layout().addLayout(self.form_layout)

        self.input_idcliente = QLineEdit()
        self.input_idcliente.setPlaceholderText("ID Cliente")
        self.input_fecha = QLineEdit()
        self.input_fecha.setPlaceholderText("Fecha")
        self.input_metopago = QLineEdit()
        self.input_metopago.setPlaceholderText("Metodo Pago")
        self.input_total = QLineEdit()
        self.input_total.setPlaceholderText("Total")

        for input_widget in (
            self.input_idcliente,
            self.input_fecha,
            self.input_metopago,
            self.input_total
        ):
            self.form_layout.addWidget(input_widget)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar Venta")
        self.btn_agregar.clicked.connect(self.agregar_venta)
        botones_layout.addWidget(self.btn_agregar)

        # self.btn_eliminar = QPushButton("Eliminar proveedor seleccionado")
        # self.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        # botones_layout.addWidget(self.btn_eliminar)

        self.layout().addLayout(botones_layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID Venta", "ID Cliente", "Fecha", "Metodo Pago", "Total"])
        
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

        self.cargar_venta()

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

    def cargar_venta(self):
        self.tabla.setRowCount(0)
        ventas = obtener_venta()
        for i, ventas in enumerate(ventas):
            self.tabla.insertRow(i)
            for j in range(5):
                self.tabla.setItem(i, j, QTableWidgetItem(str(ventas[j])))

    def agregar_venta(self):
        idcliente = self.input_idcliente.text()
        fecha = self.input_fecha.text()
        metopago = self.input_metopago.text()
        total = self.input_total.text()

        if not idcliente:
            QMessageBox.warning(self, "Error", "El ID del Cliente es Obligatorio")
            return

        agregar_venta(idcliente, fecha, metopago, total)
        QMessageBox.information(self, "Éxito", "Venta Registrada")
        self.input_idcliente.clear()
        self.input_fecha.clear()
        self.input_metopago.clear()
        self.input_total.clear()
        self.cargar_venta()

    # def eliminar_seleccionado(self):
    #     fila = self.tabla.currentRow()
    #     if fila < 0:
    #         QMessageBox.warning(self, "Error", "Selecciona un proveedor primero.")
    #         return

    #     id_item = self.tabla.item(fila, 0)
    #     if id_item:
    #         id_proveedor = int(id_item.text())
    #         confirm = QMessageBox.question(
    #             self,
    #             "Confirmar",
    #             f"¿Eliminar al proveedor con ID {id_proveedor}?",
    #             QMessageBox.Yes | QMessageBox.No
    #         )
    #         if confirm == QMessageBox.Yes:
    #             eliminar_proveedor(id_proveedor)
    #             QMessageBox.information(self, "Eliminado", "Proveedor eliminado con éxito.")
    #             self.cargar_proveedores()