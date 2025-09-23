from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QDateEdit, QDoubleSpinBox,
    QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QIcon
from controllers.productos_controller import ProductosController

class DescuentoDialog(QDialog):
    def __init__(self, id_producto, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de Oferta")
        self.controller = ProductosController()
        self.id_producto = id_producto
        self.setFixedSize(400, 300)
        
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }

            QFormLayout QLabel {
                min-width: 110px;
            }

            QDialog {
                background-color: #f2f2f2;
                font-family: Segoe UI, sans-serif;
            }

            QDoubleSpinBox, QDateEdit {
                padding: 6px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #ccc;
                background-color: #ffffff;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 5px;
            }

            QPushButton#Eliminar {
                background-color: #d9534f;
            }

            QPushButton#Cancelar {
                background-color: #6c757d;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton#Eliminar:hover {
                background-color: #c9302c;
            }

            QPushButton#Cancelar:hover {
                background-color: #5a6268;
            }

            QLabel#Estado {
                margin: 10px;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout(self)

        self.lbl_estado = QLabel("")
        self.lbl_estado.setObjectName("Estado")
        layout.addWidget(self.lbl_estado)

        form = QFormLayout()
        self.spin_descuento = QDoubleSpinBox()
        self.spin_descuento.setSuffix(" %")
        self.spin_descuento.setRange(1, 100)
        self.spin_descuento.setDecimals(1)

        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate())

        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate().addDays(7))

        form.addRow("Descuento:", self.spin_descuento)
        form.addRow("Fecha inicio:", self.date_inicio)
        form.addRow("Fecha fin:", self.date_fin)
        layout.addLayout(form)

        # Botones
        btns = QHBoxLayout()
        self.btn_guardar = QPushButton()
        self.btn_guardar.setIcon(QIcon("assets/icons/guardar.png"))
        self.btn_guardar.setText("Guardar")
        
        self.btn_eliminar = QPushButton()
        self.btn_eliminar.setIcon(QIcon("assets/icons/eliminar2.png"))
        self.btn_eliminar.setText("Eliminar")
        self.btn_eliminar.setObjectName("Eliminar")
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("Cancelar")

        self.btn_guardar.clicked.connect(self.guardar_oferta)
        self.btn_eliminar.clicked.connect(self.eliminar_oferta)
        self.btn_cancelar.clicked.connect(self.reject)

        btns.addWidget(self.btn_guardar)
        btns.addWidget(self.btn_eliminar)
        btns.addStretch()
        btns.addWidget(self.btn_cancelar)
        layout.addLayout(btns)

        self.load_oferta_actual()

    def load_oferta_actual(self):
        oferta = self.controller.obtener_oferta_por_producto(self.id_producto)
        if oferta:
            self.oferta_id = oferta.id_oferta
            self.spin_descuento.setValue(oferta.porcentaje_descuento)
            self.date_inicio.setDate(QDate.fromString(oferta.fecha_inicio, "yyyy-MM-dd"))
            self.date_fin.setDate(QDate.fromString(oferta.fecha_fin, "yyyy-MM-dd"))

            hoy = QDate.currentDate()
            if hoy >= self.date_inicio.date() and hoy <= self.date_fin.date():
                self.lbl_estado.setText('<img src="assets/icons/check.png" width="16" height="16"> Oferta activa')
            else:
                self.lbl_estado.setText('<img src="assets/icons/reloj_de_arena.png" width="16" height="16"> Oferta programada o vencida')
        else:
            self.oferta_id = None
            self.lbl_estado.setText('<img src="assets/icons/signo_de_exclamacion.png" width="16" height="16"> No hay oferta activa')

    def guardar_oferta(self):
        descuento = self.spin_descuento.value()
        inicio = self.date_inicio.date().toString("yyyy-MM-dd")
        fin = self.date_fin.date().toString("yyyy-MM-dd")

        if self.oferta_id:
            self.controller.actualizar_oferta(self.oferta_id, descuento, inicio, fin)
        else:
            self.controller.agregar_oferta(self.id_producto, descuento, inicio, fin)

        QMessageBox.information(self, "Éxito", "La oferta fue guardada correctamente.")
        self.accept()

    def eliminar_oferta(self):
        if not self.oferta_id:
            QMessageBox.warning(self, "Atención", "No hay oferta que eliminar.")
            return

        confirm = QMessageBox.question(self, "¿Eliminar?",
            "¿Seguro que quieres eliminar esta oferta?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.controller.eliminar_oferta(self.oferta_id)
            QMessageBox.information(self, "Eliminado", "Oferta eliminada.")
            self.accept()
