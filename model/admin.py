from conexionBD import Conexiones
from tkinter import *
from tkinter import messagebox
import mysql.connector
# REMOVIDO: import hashlib (Ya no se usa)


class Consultas_admins:
    
    # REMOVIDO: @staticmethod def hash_password(password): ...
    
    # --- MÉTODO 1: REGISTRAR ADMIN (Usa texto plano) ---
    # Nota: Quitamos 'self' del registro para que sea estático y funcione con el modelo.
    @staticmethod 
    def registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado):
        try:
            cone = Conexiones()
            # Asumimos que conexion_bd() retorna (conexion, cursor)
            conexion, cursor = cone.conexion_bd() 
            
            if conexion is None: return False

            try: 
                cursor = conexion.cursor()
                
                # Usamos la contraseña PLANA directamente en la consulta
                sql = """
                INSERT INTO admin (nombre, apellido_paterno, apellido_materno, mail, password, estado) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (nombre, apellido_paterno, apellido_materno, mail, password, estado) 
                
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
            except mysql.connector.Error as err:
                print(f"ERROR SQL: {err}")
                return False
        except Exception as e:
                # print(f"ERROR GENERAL: {e}") # Debugging
                return False

    # --- MÉTODO 2: VALIDAR LOGIN (Usa texto plano) ---
    @staticmethod
    def login_admin(mail, password_ingresada):
        """
        Verifica las credenciales comparando el texto plano ingresado con el texto plano en la BD.
        """
        try:
            cone = Conexiones()
            conexion, cursor = cone.conexion_bd() 
            
            if conexion is None: return None

            # 1. Consulta la BD comparando el texto plano
            sql = "SELECT id, nombre, rol FROM admin WHERE mail = %s AND password = %s AND estado = 1"
            valores = (mail, password_ingresada) # Se usa el password sin hashear
            
            cursor.execute(sql, valores)
            resultado = cursor.fetchone() 
            
            cursor.close()
            conexion.close()
            return resultado
            
        except Exception as e:
            # print(f"ERROR en login: {e}") # Debugging
            return None