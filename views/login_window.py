from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

USERS = {
    "admin": "admin123",
    "user1": "password1"
}

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar sesión")
        layout = QVBoxLayout()

        self.user_label = QLabel("Usuario:")
        self.user_input = QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        self.pass_label = QLabel("Contraseña:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)

        self.login_button = QPushButton("Ingresar")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.accepted_user = None

    def check_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        if USERS.get(username) == password:
            self.accepted_user = username
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")