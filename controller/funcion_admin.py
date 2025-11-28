from conexionBD import Conexiones
from tkinter import messagebox
import mysql.connector
# REMOVIDO: import hashlib

class Consultas_admins:
    
    # --- MÉTODO 1: REGISTRAR ADMIN (Usa texto plano) ---
    @staticmethod 
    def registrar_admin(nombre, apellido_paterno, apellido_materno, mail, password, estado):
        try:
            cone = Conexiones()
            conexion, cursor = cone.conexion_bd() 
            
            if conexion is None: return False

            try: 
                cursor = conexion.cursor()
                
                # LA CONTRASEÑA ES INSERTADA EN TEXTO PLANO
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
                print(f"ERROR GENERAL: {e}")
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

            # Consulta a la BD (TEXTO PLANO vs TEXTO PLANO)
            sql = "SELECT id, nombre, rol FROM admin WHERE mail = %s AND password = %s AND estado = 1"
            valores = (mail, password_ingresada)
            
            cursor.execute(sql, valores)
            resultado = cursor.fetchone() 
            
            cursor.close()
            conexion.close()
            return resultado
            
        except Exception as e:
            print(f"ERROR en login: {e}")
            return None