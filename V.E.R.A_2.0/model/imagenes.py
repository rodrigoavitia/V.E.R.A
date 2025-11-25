from conexionBD import Conexiones
from tkinter import messagebox
import io 

class Consultas_reportes:
    @staticmethod
    # --- CORRECCIÓN: Ahora aceptamos fecha_ini y fecha_fin ---
    def buscar_reportes(termino="", rol="Todos", fecha_ini="", fecha_fin=""):
        try:
            mi_conexion = Conexiones()
            conexion, cursor = mi_conexion.conexion_bd()
            
            if conexion and cursor:
                # Consulta Base
                sql = """
                SELECT 
                    i.fecha,
                    CONCAT(u.nombre, ' ', u.apellido_paterno) as nombre_completo,
                    u.tipo as rol_usuario,
                    u.id as matricula_usuario, 
                    v.placa,
                    'A-01' as espacio, 
                    i.hora as entrada,
                    ADDTIME(i.hora, '04:00:00') as salida,
                    i.tipo as reporte_tipo,
                    i.id as id_reporte 
                FROM imagenes i
                JOIN vehiculos v ON i.id_vehiculo = v.id
                JOIN usuarios u ON v.id_usuario = u.id
                WHERE (v.placa LIKE %s OR u.nombre LIKE %s OR u.apellido_paterno LIKE %s)
                """
                
                params = [f"%{termino}%", f"%{termino}%", f"%{termino}%"]

                # --- FILTRO DE ROL ---
                if rol != "Todos" and rol != "Tipo de usuario":
                    sql += " AND u.tipo = %s"
                    params.append(rol)

                # --- FILTRO DE FECHAS (NUEVO) ---
                if fecha_ini and fecha_fin:
                    sql += " AND i.fecha BETWEEN %s AND %s"
                    params.append(fecha_ini)
                    params.append(fecha_fin)
                elif fecha_ini:
                    sql += " AND i.fecha >= %s"
                    params.append(fecha_ini)

                sql += " ORDER BY i.fecha DESC, i.hora DESC LIMIT 50"
                
                cursor.execute(sql, tuple(params))
                resultados = cursor.fetchall()
                
                cursor.close()
                conexion.close()
                return resultados
            
            return []
            
        except Exception as e:
            print(f"Error buscando reportes: {e}")
            return []

    @staticmethod
    def obtener_detalle(id_reporte):
        """Recupera la imagen BLOB y datos completos"""
        try:
            mi_conexion = Conexiones()
            conexion, cursor = mi_conexion.conexion_bd()
            
            if conexion and cursor:
                sql = """
                SELECT i.imagen, i.fecha, i.hora, i.tipo, v.placa, v.modelo, v.color,
                       CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', u.apellido_materno) as nombre,
                       u.tipo as rol
                FROM imagenes i
                JOIN vehiculos v ON i.id_vehiculo = v.id
                JOIN usuarios u ON v.id_usuario = u.id
                WHERE i.id = %s
                """
                cursor.execute(sql, (id_reporte,))
                resultado = cursor.fetchone()
                
                cursor.close()
                conexion.close()
                return resultado
        except Exception as e:
            print(f"Error obteniendo detalle: {e}")
            return None