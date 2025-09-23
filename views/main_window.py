# views/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QLineEdit, QListWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Sistema de Productos")
        self.setGeometry(100, 100, 800, 600)
        # Fondo sólido
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: #2c3e50;
                font-size: 18px;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }
            QListWidget {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                font-size: 16px;
            }
        """)

        # Estado del menú
        self.menu_expanded = True

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Menú lateral 
        self.menu = QFrame()
        self.menu.setMaximumWidth(220)
        self.menu.setMinimumWidth(60)
        self.menu.setStyleSheet("background-color: #2F3542;")
        menu_layout = QVBoxLayout(self.menu)
        menu_layout.setContentsMargins(0, 10, 0, 10)
        menu_layout.setSpacing(5)

        self.btn_toggle = QPushButton()
        self.btn_toggle.setIcon(QIcon("assets/icons/cerrar.png"))
        self.btn_toggle.setToolTip("Cerrar menú")
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.setFixedSize(40, 40)
        self.btn_toggle.setStyleSheet("color: white; background: transparent; border: none;")
        self.btn_toggle.clicked.connect(self.toggle_menu)
        menu_layout.addWidget(self.btn_toggle, alignment=Qt.AlignRight)

        self.title = QLabel("SCALE")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white; font-size: 26px; font-weight: bold;")
        menu_layout.addWidget(self.title)

        self.buttons = []
        specs = [
            ("Productos",  "assets/icons/productos.png", self.show_productos),
            ("Clientes",   "assets/icons/clientes.png",  self.show_clientes),
            ("Proveedores","assets/icons/proveedores.png", self.show_proveedores),
            ("Ventas",     "assets/icons/ventas.png",     self.show_ventas),
            ("Salir",      "assets/icons/salir.png",      self.close_Window),
        ]
        for text, icon_path, slot in specs[:-1]:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(40)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24,24))
            btn.setToolTip(text)
            btn.setProperty("full_text", text)
            btn.clicked.connect(slot)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding-left: 10px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #57606f;
                }
            """)
            menu_layout.addWidget(btn)
            self.buttons.append(btn)

        menu_layout.addStretch()
        
        # Botón de salir hasta la parte inferior del menú
        text, icon, slot = specs[-1]
        btn_exit = QPushButton(text)
        btn_exit.setCursor(Qt.PointingHandCursor)
        btn_exit.setFixedHeight(40)
        btn_exit.setIcon(QIcon(icon))
        btn_exit.setIconSize(QSize(24, 24))
        btn_exit.setToolTip(text)
        btn_exit.setProperty("full_text", text)
        btn_exit.clicked.connect(slot)
        btn_exit.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #57606f;
            }
        """)
        menu_layout.addWidget(btn_exit)
        self.buttons.append(btn_exit)
        root_layout.addWidget(self.menu)


        self.content = QFrame()
        self.content.setStyleSheet("background-color: #f1f2f6;")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout = content_layout
        root_layout.addWidget(self.content)

        self.show_home()

    def toggle_menu(self):
        self.menu_expanded = not self.menu_expanded
        new_width = 220 if self.menu_expanded else 60

        # Animación
        self.animation = QPropertyAnimation(self.menu, b"maximumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.menu.width())
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

        self.btn_toggle.setIcon(QIcon("assets/icons/cerrar.png") if self.menu_expanded else QIcon("assets/icons/barras_menu.png"))
        self.title.setVisible(self.menu_expanded)
        self.btn_toggle.setToolTip("Cerrar menú" if self.menu_expanded else "Abrir menú")

        for btn in self.buttons:
            full_text = btn.property("full_text")
            btn.setText(full_text if self.menu_expanded else "")
            btn.setToolTip("" if self.menu_expanded else full_text)

    def clear_content(self):
        # Limpia la vista actual
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.takeAt(i).widget()
            if widget:
                widget.setParent(None)

    def show_home(self):
        self.clear_content()
        label = QLabel("Bienvenido a SCALE-System")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 22px;")
        self.content_layout.addWidget(label)

    def show_productos(self):
        self.clear_content()
        try:
            from views.productos_view import ProductosView
            self.content_layout.addWidget(ProductosView())
        except Exception as e:
            error_label = QLabel(f"Error al cargar productos:\n{e}")
            error_label.setStyleSheet("color: red; font-size: 16px;")
            self.content_layout.addWidget(error_label)

    def show_clientes(self):
        from views.clientes_view import ClientesView
        self.clear_content()
        self.content_layout.addWidget(ClientesView())

    def show_proveedores(self):
        from views.proveedores_view import ProveedoresView
        self.clear_content()
        self.content_layout.addWidget(ProveedoresView())

    def show_ventas(self):
        from views.ventas_view import VentaView
        self.clear_content()
        self.content_layout.addWidget(VentaView())
        
    def close_Window(self):
        self.close()