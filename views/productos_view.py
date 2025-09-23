from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QTableWidget, QHeaderView, QComboBox, QSizePolicy, QFrame, QDialog, QMessageBox, QFileDialog, QTableWidgetItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor
from controllers.productos_controller import ProductosController

from views.producto_dialog import ProductoDialog
from views.descuento_dialog import DescuentoDialog

from utils.export_utils import (
    exportar_productos_a_excel,
    exportar_productos_a_pdf
)

class ProductosView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ProductosController()

        self.setStyleSheet("""
            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 10px;
                color: #222;
            }

            QLabel {
                color: #222;
            }

            QPushButton#btnAdd {
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton#btnExcel {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton#btnPdf {
                background-color: #c0392b;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton#actionButton {
                background: transparent;
                border: none;
                padding: 5px;
            }

            QComboBox, QLineEdit {
                padding: 6px 10px;
                border: 2px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
                color: #222;
                background: #fff;
            }

            QComboBox::drop-down {
                width: 30px;
                border: none;
            }

            QComboBox::down-arrow {
                image: url(assets/icons/down_arrow.png); 
                width: 26px;
            }

            QTableWidget {
                background-color: #fdfefe;
                alternate-background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                font-size: 14px;
                border-radius: 8px;
                color: #222;
            }

            QHeaderView::section {
                background-color: #34495e;
                color: white;
                font-size: 14px;
                padding: 6px;
                border: none;
            }

            QTableWidget::item {
                border-bottom: 1px solid #dcdcdc;
                padding: 4px;
                color: #222;
            }

            QTableWidget::item:selected {
                background-color: #aed6f1;
                color: #222;
            }
        """)

        layout = QVBoxLayout(self)

        # Título
        title = QLabel("Gestión de Productos")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        buttons = QHBoxLayout()
        self.btn_add = QPushButton()
        self.btn_add.setIcon(QIcon("assets/icons/agregar_producto2.png"))
        self.btn_add.setText("Agregar Producto")
        self.btn_add.clicked.connect(self.add_product)
        
        self.btn_excel = QPushButton()
        self.btn_excel.setIcon(QIcon("assets/icons/excel.png"))
        self.btn_excel.setText("Exportar a Excel")
        self.btn_excel.clicked.connect(self.save_to_excel)
        
        self.btn_pdf = QPushButton()
        self.btn_pdf.setIcon(QIcon("assets/icons/pdf.png"))
        self.btn_pdf.setText("Exportar a PDF")
        self.btn_pdf.clicked.connect(self.save_to_pdf)

        self.btn_add.setObjectName("btnAdd")
        self.btn_excel.setObjectName("btnExcel")
        self.btn_pdf.setObjectName("btnPdf")

        for btn in (self.btn_add, self.btn_excel, self.btn_pdf):
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            buttons.addWidget(btn)
        buttons.addStretch()
        layout.addLayout(buttons)

        # filters: combo + búsqueda
        filters = QHBoxLayout()
        self.cmb_category = QComboBox()
        self.cmb_category.addItem("Todas las Categorías")
        for c in self.controller.obtener_categorias():
            self.cmb_category.addItem(c.nombre,c.id_categoria)

        self.cmb_supplier = QComboBox()
        self.cmb_supplier.addItem("Todos los Proveedores")
        for p in self.controller.obtener_proveedores():
            self.cmb_supplier.addItem(p.nombre, p.id_proveedor)
        
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Buscar producto...")
        
        self.cmb_category.currentIndexChanged.connect(self.load_data)
        self.cmb_supplier.currentIndexChanged.connect(self.load_data)
        self.txt_search.textChanged.connect(self.load_data)

        for f in (self.cmb_category, self.cmb_supplier, self.txt_search):
            f.setFixedHeight(32)
            filters.addWidget(f)
        filters.addStretch()
        layout.addLayout(filters)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Descripción", "Precio", "Stock", "Proveedor", "Categoría", "Acciones"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)          
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(5, QHeaderView.Stretch)           
        header.setSectionResizeMode(6, QHeaderView.Stretch)           
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  
        
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(40)  
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)

        # Obtener valores de filtros
        categoria_id = self.cmb_category.currentData()
        proveedor_id = self.cmb_supplier.currentData()
        texto_busqueda = self.txt_search.text().lower()

        productos = self.controller.obtener_productos_con_stock()

        # Filtrar
        productos_filtrados = []
        for p in productos:
            id_prod, nombre, descripcion, precio_base, stock, proveedor, categoria = p
            if categoria_id and categoria != self.cmb_category.currentText():
                continue
            if proveedor_id and proveedor != self.cmb_supplier.currentText():
                continue
            if texto_busqueda and texto_busqueda not in f"{nombre} {descripcion}".lower():
                continue
            productos_filtrados.append(p)

        for row_idx, prod in enumerate(productos_filtrados):
            self.table.insertRow(row_idx)
            id_prod, nombre, descripcion, precio_base, stock, proveedor, categoria = prod

            # 0 ID
            item = QTableWidgetItem(str(id_prod))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 0, item)

            # 1 Nombre
            item = QTableWidgetItem(nombre)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 1, item)

            # 2 Descripción
            item = QTableWidgetItem(descripcion)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 2, item)

            # 3 Precio (con descuento si aplica)
            oferta = self.controller.obtener_oferta_por_producto(id_prod)
            if oferta:
                precio_oferta = round(precio_base * (1 - oferta.porcentaje_descuento / 100), 2)
                item_precio = QTableWidgetItem(f"${precio_oferta:.2f}")
                item_precio.setForeground(QColor("#3CB371"))
                item_precio.setToolTip(
                    f"Precio con oferta: ${precio_oferta:.2f}\n"
                    f"Precio original: ${precio_base:.2f}\n"
                    f"Descuento: {oferta.porcentaje_descuento}%"
                )
            else:
                item_precio = QTableWidgetItem(f"${precio_base:.2f}")
            item_precio.setFlags(item_precio.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 3, item_precio)

            # 4 Stock
            item = QTableWidgetItem(str(stock))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 4, item)

            # 5 Proveedor
            item = QTableWidgetItem(proveedor)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 5, item)

            # 6 Categoría
            item = QTableWidgetItem(categoria)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 6, item)

            # 7 Acciones (editar, eliminar, oferta)
            frame = QFrame()
            frame.setStyleSheet("background-color: transparent;")
            hl = QHBoxLayout(frame)
            hl.setContentsMargins(0, 0, 0, 0)

            btn_edit = QPushButton()
            btn_edit.setIcon(QIcon("assets/icons/editar.png"))
            btn_delete = QPushButton()
            btn_delete.setIcon(QIcon("assets/icons/eliminar.png"))
            btn_offer = QPushButton()
            btn_offer.setIcon(QIcon("assets/icons/oferta2.png"))

            btn_edit.clicked.connect(lambda _, id=id_prod: self.edit_product(id))
            btn_delete.clicked.connect(lambda _, id=id_prod: self.delete_product(id))
            btn_offer.clicked.connect(lambda _, id=id_prod: self.manage_offer(id))

            for btn, tip in (
                (btn_edit, "Editar"),
                (btn_delete, "Eliminar"),
                (btn_offer, "Oferta")
            ):
                btn.setCursor(Qt.PointingHandCursor)
                btn.setIconSize(QSize(20, 20))
                btn.setToolTip(tip)
                btn.setFixedSize(30, 30)
                btn.setObjectName("actionButton")
                hl.addWidget(btn)

            hl.addStretch()
            self.table.setCellWidget(row_idx, 7, frame)

    
    def add_product(self):
        #Abre diálogo en modo Agregar
        dlg = ProductoDialog(None, parent=self)
        if dlg.exec() == QDialog.Accepted:
            self.load_data()
    
    def edit_product(self, id_producto):
        #Abre diálogo en modo Editar con datos llenados del producto
        producto = self.controller.obtener_producto(id_producto)
        if not producto:
            QMessageBox.warning(self, "Error", "Producto no encontrado.")
            return

        dlg = ProductoDialog(producto, parent=self)
        if dlg.exec() == QDialog.Accepted:
            self.load_data()

    def delete_product(self, id_producto):
        confirm = QMessageBox.question(
            self, "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar este producto Y todas sus variantes?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.eliminar_producto(id_producto)
            self.load_data()
        
    def manage_offer(self, id_producto):
        dlg = DescuentoDialog(id_producto, parent=self)
        if dlg.exec() == QDialog.Accepted:
            self.load_data()
    
    def save_to_excel(self):
        productos = self.controller.obtener_productos_con_variantes()
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar como Excel", "Reporte_Productos.xlsx",
            "Archivos Excel (*.xlsx)"
        )
        if ruta:
            if not ruta.lower().endswith(".xlsx"):
                ruta += ".xlsx"
            exportar_productos_a_excel(productos, ruta)
            QMessageBox.information(self, "Éxito", f"Excel guardado en:\n{ruta}")

    def save_to_pdf(self):
        productos = self.controller.obtener_productos_con_variantes()
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar como PDF", "Reporte_Productos.pdf",
            "Archivos PDF (*.pdf)"
        )
        if ruta:
            if not ruta.lower().endswith(".pdf"):
                ruta += ".pdf"
            exportar_productos_a_pdf(productos, ruta)
            QMessageBox.information(self, "Éxito", f"PDF guardado en:\n{ruta}")