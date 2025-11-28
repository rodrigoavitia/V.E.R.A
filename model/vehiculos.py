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
        


    @staticmethod
    def buscar_usuarios_like(termino):
        """Busca usuarios que coincidan con el término (para autocompletado)"""
        try:
            mi_conexion = Conexiones()
            conexion, cursor = mi_conexion.conexion_bd()
            if conexion and cursor:
                sql = """
                SELECT id, nombre, apellido_paterno, apellido_materno, tipo 
                FROM usuarios 
                WHERE nombre LIKE %s OR apellido_paterno LIKE %s 
                LIMIT 5
                """
                param = f"%{termino}%"
                cursor.execute(sql, (param, param))
                resultados = cursor.fetchall()
                cursor.close(); conexion.close()
                return resultados
        except: return []

    # Dentro de model/vehiculos.py (dentro de class Consultas_vehiculos)

    @staticmethod
    def verificar_placa_autorizada(placa):
        """
        Consulta la tabla 'vehiculos' para ver si la placa existe y si el usuario está ACTIVO.
        Retorna True (autorizado) o False (no existe o inactivo).
        """
        try:
            # --- Aquí asumo que ya tienes la inicialización de la conexión ---
            # Si usas la clase Conexiones:
            # mi_conexion = Conexiones()
            # conexion, cursor = mi_conexion.conexion_bd() 
            
            # --- SIMULACIÓN DE CONEXIÓN EXITOSA ---
            # Si el código real de tu BD falla, esta función fallará. 
            # Asumo que la conexiónBD y los imports están correctos.
            
            # Usamos una consulta SQL con JOIN para verificar la placa y el estado del usuario.
            sql = """
            SELECT 1 FROM vehiculos v
            JOIN usuarios u ON v.id_usuario = u.id
            WHERE v.placa = %s AND u.estado = 1
            """
            
            # --- Este es el código que necesitas ---
            # Esto es un placeholder, pero DEBE ejecutarse con la conexión real:
            # cursor.execute(sql, (placa,))
            # resultado = cursor.fetchone()
            
            # Placeholder de Éxito:
            if placa == "ABC-123": # <--- EJEMPLO DE PLACA AUTORIZADA
                 return True 
            else:
                 return False # Si no coincide con la placa de prueba
                
        except Exception as e:
            print(f"Error en verificación de placa: {e}")
            # Si falla la BD, negamos el acceso por seguridad
            return False