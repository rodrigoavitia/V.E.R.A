import mysql.connector
from tkinter import messagebox

class Conexiones:
    def conexion_bd(self):
        try:
            # Ajusta tus credenciales si es necesario
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bd_estacionamiento"
            )
            cursor = conexion.cursor()
            return conexion, cursor
            
        except Exception as e:
            # Usamos messagebox aquí solo para reportar el error crítico
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {e}")
            return None, None