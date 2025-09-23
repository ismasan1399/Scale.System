import sqlite3

class DatabaseConnection:
    def __init__(self, db_path="database/scale_system.db", auto_connect=True):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        if auto_connect:
            self.connect()

    def connect(self):
        if not self.connection:
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()
                print("Conexión a la base de datos establecida.")
            except sqlite3.Error as e:
                print(f"Error al conectar con la base de datos: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Conexión a la base de datos cerrada.")

    def execute(self, query, params=None, commit=False):
        try:
            if not self.connection:
                self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if commit:
                self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def executemany(self, query, param_list, commit=False):
        try:
            if not self.connection:
                self.connect()
            self.cursor.executemany(query, param_list)
            if commit:
                self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error al ejecutar múltiples consultas: {e}")
            return None

    def commit(self):
        try:
            if self.connection:
                self.connection.commit()
                print("Cambios guardados en la base de datos.")
            else:
                print("No hay conexión para guardar cambios.")
        except sqlite3.Error as e:
            print(f"Error al guardar cambios: {e}")
