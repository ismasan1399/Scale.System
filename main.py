import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow
from views.login_window import LoginWindow  # <-- Importa la ventana de login

def main():
    app = QApplication(sys.argv)

    # Muestra la ventana de login primero
    login = LoginWindow()
    if login.exec() == LoginWindow.Accepted:
        # Si el login es correcto, muestra la ventana principal
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        # Si el login falla o se cierra, termina la app
        sys.exit()

if __name__ == "__main__":
    main()
