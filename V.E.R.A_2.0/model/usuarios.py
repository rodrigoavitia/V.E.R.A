from conexionBD import Conexiones
from tkinter import messagebox

class Consulta_usuarios:
    @staticmethod
    def registrar_persona(nombre, ape_pat, ape_mat, rol, estado, email=None, password=None):
        try:
            mi_conexion = Conexiones()
            conexion, cursor = mi_conexion.conexion_bd()
            
            if conexion and cursor:
                # Convertir bool a int (1 o 0)
                estado_int = 1 if estado else 0
                
                if "Sudito" in rol:
                    # Tabla ADMIN
                    sql = """
                    INSERT INTO admin (nombre, apellido_paterno, apellido_materno, mail, password, estado, rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    valores = (nombre, ape_pat, ape_mat, email, password, estado_int, "Administrador")
                else:
                    # Tabla USUARIOS
                    sql = """
                    INSERT INTO usuarios (nombre, apellido_paterno, apellido_materno, tipo, estado)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    valores = (nombre, ape_pat, ape_mat, rol, estado_int)

                cursor.execute(sql, valores)
                conexion.commit()
                
                cursor.close()
                conexion.close()
                return True
            else:
                return False
                
        except Exception as e:
            messagebox.showerror("Error de BD", f"No se pudo guardar el registro: {e}")
            return False