import mysql.connector
from tkinter import messagebox
from view import interface

class Conexiones:
    @staticmethod
    def conexion_bd():
        try:
            # Intentamos conectar
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='bd_estacionamiento'
            )
            
            return conexion 
            
        except Exception as e:
            # Si falla, mostramos el error y devolvemos None
            print(f"❌ Error en conectionBD: {e}") # Para verlo en la terminal
            messagebox.showerror(
                title="ERROR de conexión", 
                message=f"Fallo al conectar con la base de datos: {e}",
                icon="error"
            )            
            return None