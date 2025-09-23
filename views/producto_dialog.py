 # views/producto_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, QLabel, QMessageBox, QComboBox, QHeaderView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


from controllers.productos_controller import ProductosController
from models.variante_producto import VarianteProducto


class VarianteDialog(QDialog):
    """Diálogo para agregar/editar una variante."""
    def __init__(self, variante: VarianteProducto = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Variante" if variante else "Agregar Variante")
        self.resize(300, 200)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
            }
            QLineEdit, QSpinBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#cancel {
                background-color: #e74c3c;
            }
            QPushButton#cancel:hover {
                background-color: #c0392b;
            }
        """)

        self.variante = variante
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.txt_talla = QLineEdit(variante.talla if variante else "")
        self.txt_color = QLineEdit(variante.color if variante else "")
        self.spn_stock = QSpinBox()
        self.spn_stock.setRange(0, 100000)
        self.spn_stock.setValue(variante.stock if variante else 0)

        form.addRow("Talla:", self.txt_talla)
        form.addRow("Color:", self.txt_color)
        form.addRow("Stock:", self.spn_stock)
        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_ok = QPushButton("Aceptar")
        btn_ok.setCursor(Qt.PointingHandCursor)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setObjectName("cancel")
        
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        btns.addStretch()
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    def get_data(self):
        #Devuelve (talla, color, stock)
        return (
            self.txt_talla.text().strip(),
            self.txt_color.text().strip(),
            self.spn_stock.value()
        )


class ProductoDialog(QDialog):
    def __init__(self, producto=None, parent=None):
        super().__init__(parent)
        self.producto = producto
        self.ctrl = ProductosController()
        self.is_new = producto is None
        self.variantes_temp = []  # Lista de variantes para cuando se crea un nuevo producto

        self.setWindowTitle("Agregar Producto" if self.is_new else "Editar Producto")
        self.resize(700, 600)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QSpinBox {
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 14px;
            }
            
            /* buttons de acción en tabla */
            QPushButton#actionButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            
            QPushButton#cancel {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #219653;
            }
            QPushButton#cancel:hover {
                background-color: #c0392b;
            }
            QTableWidget {
                border: 1px solid #d0d0d0;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 6px;
                font-size: 13px;
            }
        """)

        main = QVBoxLayout(self)

        #  Campos producto 
        form = QFormLayout()
        self.txt_nombre = QLineEdit(producto.nombre if producto else "")
        self.txt_descripcion = QLineEdit(producto.descripcion if producto else "")
        self.spn_precio = QSpinBox()
        self.spn_precio.setRange(0, 1000000)
        self.spn_precio.setValue(int(producto.precio_base) if producto else 0)

        # Cargar proveedores y categorías
        self.cmb_proveedor = QComboBox()
        for p in self.ctrl.obtener_proveedores():
            self.cmb_proveedor.addItem(p.nombre, p.id_proveedor)
        if not self.is_new:
            idx = self.cmb_proveedor.findData(producto.id_proveedor)
            self.cmb_proveedor.setCurrentIndex(idx)

        self.cmb_categoria = QComboBox()
        for c in self.ctrl.obtener_categorias():
            self.cmb_categoria.addItem(c.nombre, c.id_categoria)
        if not self.is_new:
            idx = self.cmb_categoria.findData(producto.id_categoria)
            self.cmb_categoria.setCurrentIndex(idx)

        form.addRow("Nombre:", self.txt_nombre)
        form.addRow("Descripción:", self.txt_descripcion)
        form.addRow("Precio base:", self.spn_precio)
        form.addRow("Proveedor:", self.cmb_proveedor)
        form.addRow("Categoría:", self.cmb_categoria)
        main.addLayout(form)

        #  Tabla de variantes 
        lbl = QLabel("Variantes:")
        main.addWidget(lbl)

        self.tbl_var = QTableWidget(0, 4)
        self.tbl_var.setHorizontalHeaderLabels(["Talla", "Color", "Stock", "Acciones"])
        self.tbl_var.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tbl_var.verticalHeader().setVisible(False)
        main.addWidget(self.tbl_var)

        hb = QHBoxLayout()
        btn_add_var = QPushButton()
        btn_add_var.setIcon(QIcon("assets/icons/agregar.png"))
        btn_add_var.setText("Agregar Variante")
        btn_add_var.clicked.connect(self.on_add_variante)
        hb.addWidget(btn_add_var)
        hb.addStretch()
        main.addLayout(hb)

        footer = QHBoxLayout()
        btn_save = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("cancel")
        btn_save.clicked.connect(self.on_save)
        btn_cancel.clicked.connect(self.reject)
        footer.addStretch()
        footer.addWidget(btn_save)
        footer.addWidget(btn_cancel)
        main.addLayout(footer)

        # Cargar variantes si se está editando
        if not self.is_new:
            self.load_variantes()

    def load_variantes(self):
        self.tbl_var.setRowCount(0)
        variantes = self.ctrl.obtener_variantes(self.producto.id_producto)
        for v in variantes:
            self._add_variante_row(v)

    def _add_variante_row(self, variante: VarianteProducto):
        i = self.tbl_var.rowCount()
        self.tbl_var.insertRow(i)
        self.tbl_var.setItem(i, 0, QTableWidgetItem(variante.talla))
        self.tbl_var.setItem(i, 1, QTableWidgetItem(variante.color))
        self.tbl_var.setItem(i, 2, QTableWidgetItem(str(variante.stock)))

        # Botones acciones
        cell = QWidget()
        hb = QHBoxLayout(cell)
        hb.setContentsMargins(0, 0, 0, 0)

        btn_e = QPushButton()
        btn_e.setIcon(QIcon("assets/icons/editar.png"))
        btn_e.setObjectName("actionButton")
        btn_e.setCursor(Qt.PointingHandCursor)
        
        btn_d = QPushButton()
        btn_d.setIcon(QIcon("assets/icons/eliminar.png"))
        btn_d.setObjectName("actionButton")
        btn_d.setCursor(Qt.PointingHandCursor)
        
        btn_e.clicked.connect(lambda _, vid=variante.id_variante: self.on_edit_variante(vid))
        btn_d.clicked.connect(lambda _, vid=variante.id_variante: self.on_delete_variante(vid))
        hb.addWidget(btn_e)
        hb.addWidget(btn_d)
        hb.addStretch()
        self.tbl_var.setCellWidget(i, 3, cell)

    def on_add_variante(self):
        dlg = VarianteDialog(parent=self)
        if dlg.exec() == QDialog.Accepted:
            talla, color, stock = dlg.get_data()
            if self.is_new:
                v = VarianteProducto(
                    id_variante=None,
                    id_producto=None,
                    talla=talla,
                    color=color,
                    stock=stock,
                    sku=None
                )
                self.variantes_temp.append(v)
                self._add_variante_row(v)
            else:
                v = self.ctrl.agregar_variante(
                    self.producto.id_producto, talla, color, stock
                )
                self._add_variante_row(v)

    def on_edit_variante(self, id_variante):
        # Carga la variante desde BD
        v = self.ctrl.obtener_variante(id_variante)
        dlg = VarianteDialog(v, parent=self)
        if dlg.exec() == QDialog.Accepted:
            talla, color, stock = dlg.get_data()
            self.ctrl.editar_variante(id_variante, talla, color, stock)
            self.load_variantes()

    def on_delete_variante(self, id_variante):
        if QMessageBox.question(
            self, "Confirmar", "¿Eliminar esta variante?"
        ) == QMessageBox.Yes:
            self.ctrl.eliminar_variante(id_variante)
            self.load_variantes()

    def on_save(self):
        nombre = self.txt_nombre.text().strip()
        descripcion = self.txt_descripcion.text().strip()
        precio = self.spn_precio.value()
        prov_id = self.cmb_proveedor.currentData()
        cat_id = self.cmb_categoria.currentData()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio.")
            return

        # Guardar o actualizar producto
        if self.is_new:
            prod = self.ctrl.agregar_producto(
                nombre, descripcion, precio, prov_id, cat_id
            )
            self.producto = prod
            for v in self.variantes_temp:
                self.ctrl.agregar_variante(
                    prod.id_producto, v.talla, v.color, v.stock
                )
        else:
            self.ctrl.editar_producto(
                self.producto.id_producto, nombre, descripcion,
                precio, prov_id, cat_id
            )
        self.accept()
