from conexionBD import Conexiones
from tkinter import *
from tkinter import messagebox
import mysql.connector


class Consultas_admins:
    

    def registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado):
        try:
            cone = Conexiones()
            conexion = cone.conexion_bd()
            
            if conexion is None:
                print("ERROR: cone.conexion_bd() devolvió None (Revisa conectionBD.py)")
                return False

            try:
                cursor = conexion.cursor()
                sql = f"INSERT INTO admin (id, nombre, apellido_paterno, apellido_materno, mail, password, estado) VALUES ({id}, '{nombre}', '{apellido_paterno}', '{apellido_materno}', '{mail}', '{password}', {estado});"
                print(f"SQL a ejecutar: {sql}")
                
                cursor.execute(sql)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
            except mysql.connector.Error as err:
                print(f"ERROR SQL: {err}")
                return False
        except Exception as e:
            print(f"ERROR GENERAL: {e}")
            return False


   
