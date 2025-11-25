from conexionBD import Conexiones
from tkinter import messagebox

class Consultas_vehiculos:
    
    @staticmethod
    def buscar_propietario(termino):
        """Busca un usuario por nombre o apellido y devuelve sus datos"""
        try:
            mi_conexion = Conexiones()
            conexion, cursor = mi_conexion.conexion_bd()
            
            if conexion and cursor:
                # Buscamos por nombre O apellido (LIKE permite búsquedas parciales)
                sql = """
                SELECT id, nombre, apellido_paterno, apellido_materno, tipo 
                FROM usuarios 
                WHERE nombre LIKE %s OR apellido_paterno LIKE %s 
                LIMIT 1
                """
                # Agregamos % para que busque coincidencias
                param = f"%{termino}%"
                cursor.execute(sql, (param, param))
                resultado = cursor.fetchone() # Obtenemos el primero que coincida
                
                cursor.close()
                conexion.close()
                return resultado # Devuelve una tupla (id, nombre, ape_pat, ape_mat, tipo)
            
        except Exception as e:
            messagebox.showerror("Error BD", f"Error al buscar usuario: {e}")
            return None

    @staticmethod
    def registrar_vehiculo(marca, modelo, color, placa, anio, id_usuario):
        """Registra el vehículo vinculado al ID del usuario"""
        try:
            mi_conexion = Conexiones()
            conexion, cursor = mi_conexion.conexion_bd()
            
            if conexion and cursor:
                sql = """
                INSERT INTO vehiculos (marca, modelo, color, placa, anio, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (marca, modelo, color, placa, anio, id_usuario)
                
                cursor.execute(sql, valores)
                conexion.commit()
                
                cursor.close()
                conexion.close()
                return True
                
        except Exception as e:
            # Manejo de errores (ej. placa duplicada)
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", f"La placa {placa} ya existe en el sistema.")
            else:
                messagebox.showerror("Error BD", f"No se pudo registrar vehículo: {e}")
            return False