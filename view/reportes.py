import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
from tkcalendar import Calendar
from model.imagenes import Consultas_reportes 

class ReportesView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F9FAFB")

        # --- CONTENEDOR PRINCIPAL ---
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=14, border_color="#E5E7EB", border_width=1)
        self.main_card.pack(fill="both", expand=True, padx=32, pady=32)

        # Banner FASE BETA
        self.banner = ctk.CTkFrame(self.main_card, fg_color="#10B981", height=40, corner_radius=0)
        self.banner.pack(fill="x", side="top")
        ctk.CTkLabel(self.banner, text="🚀 FASE BETA - SISTEMA DE REPORTES ACTIVO", text_color="white", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # Header
        self.header = ctk.CTkFrame(self.main_card, fg_color="transparent", height=80)
        self.header.pack(fill="x", padx=24, pady=(20, 0))
        ctk.CTkLabel(self.header, text="📄 Sistema de Reportes", font=("Arimo", 24, "bold"), text_color="#0A0A0A").pack(side="left")
        ctk.CTkButton(self.header, text="Volver", fg_color="white", text_color="#0A0A0A", border_color="#E5E7EB", border_width=1, width=80, command=self.volver).pack(side="right")
        ctk.CTkFrame(self.main_card, height=2, fg_color="#F3F4F6").pack(fill="x", pady=20)

        # --- BARRA DE FILTROS ---
        self.filters_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.filters_frame.pack(fill="x", padx=24)

        # Fila 1: Búsqueda General
        row1 = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))
        
        self.entry_search = ctk.CTkEntry(row1, placeholder_text="🔍 Buscar por Nombre, Placa...", width=300)
        self.entry_search.pack(side="left", padx=(0, 10))
        self.entry_search.bind("<Return>", self.realizar_busqueda)
        
        self.cb_filtro_rol = ctk.CTkComboBox(row1, values=["Todos", "Estudiante", "Docente", "Administrativo", "Trabajador", "Directivo"], width=150)
        self.cb_filtro_rol.set("Todos")
        self.cb_filtro_rol.pack(side="left", padx=10)

        # Fila 2: Filtros de Fecha
        row2 = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 10))

        # Fecha Desde
        ctk.CTkLabel(row2, text="Desde:", text_color="gray").pack(side="left", padx=(0, 5))
        self.entry_fecha_ini = ctk.CTkEntry(row2, placeholder_text="AAAA-MM-DD", width=100)
        self.entry_fecha_ini.pack(side="left")
        ctk.CTkButton(row2, text="📅", width=30, fg_color="#E5E7EB", text_color="black", hover_color="#D1D5DB", command=lambda: self.abrir_calendario(self.entry_fecha_ini)).pack(side="left", padx=(2, 15))

        # Fecha Hasta
        ctk.CTkLabel(row2, text="Hasta:", text_color="gray").pack(side="left", padx=(0, 5))
        self.entry_fecha_fin = ctk.CTkEntry(row2, placeholder_text="AAAA-MM-DD", width=100)
        self.entry_fecha_fin.pack(side="left")
        ctk.CTkButton(row2, text="📅", width=30, fg_color="#E5E7EB", text_color="black", hover_color="#D1D5DB", command=lambda: self.abrir_calendario(self.entry_fecha_fin)).pack(side="left", padx=(2, 20))

        # Botones Acción
        ctk.CTkButton(row2, text="🔍 Filtrar", width=100, fg_color="#0092B8", command=lambda: self.realizar_busqueda(None)).pack(side="left")
        ctk.CTkButton(row2, text="Limpiar", width=80, fg_color="transparent", border_width=1, text_color="gray", command=self.limpiar_filtros).pack(side="left", padx=10)

        # --- TABLA DE DATOS ---
        self.lbl_resultados = ctk.CTkLabel(self.main_card, text="Resultados: 0", font=("Arimo", 12, "bold"), text_color="gray")
        self.lbl_resultados.pack(anchor="w", padx=24, pady=(10, 5))

        header_cols = ["Fecha", "Nombre", "Rol", "ID Usuario", "Placa", "Espacio", "Entrada", "Salida", "Tipo", ""]
        self.widths = [90, 180, 100, 80, 100, 70, 70, 70, 90, 60]
        
        self.table_header = ctk.CTkFrame(self.main_card, fg_color="#F9FAFB", height=35, corner_radius=0)
        self.table_header.pack(fill="x", padx=24)
        for i, col in enumerate(header_cols):
            ctk.CTkLabel(self.table_header, text=col, font=("Arimo", 12, "bold"), text_color="#334155", anchor="w", width=self.widths[i]).pack(side="left", padx=5)

        self.table_body = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent", height=350)
        self.table_body.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self.realizar_busqueda(None)

    # --- FUNCIONES LÓGICAS ---

    def abrir_calendario(self, entry_target):
        top = ctk.CTkToplevel(self)
        top.title("Seleccionar Fecha")
        top.geometry("300x250")
        top.grab_set()
        try: top.geometry("+%d+%d" % (self.winfo_rootx()+50, self.winfo_rooty()+50))
        except: pass

        cal = Calendar(top, selectmode='day', locale='es_ES', date_pattern='y-mm-dd')
        cal.pack(pady=20, padx=20, fill="both", expand=True)

        def seleccionar():
            fecha = cal.get_date()
            entry_target.delete(0, 'end')
            entry_target.insert(0, fecha)
            top.destroy()

        ctk.CTkButton(top, text="Seleccionar", command=seleccionar).pack(pady=10)

    def realizar_busqueda(self, event):
        termino = self.entry_search.get()
        rol = self.cb_filtro_rol.get()
        f_ini = self.entry_fecha_ini.get()
        f_fin = self.entry_fecha_fin.get()
        
        for widget in self.table_body.winfo_children(): widget.destroy()
            
        resultados = Consultas_reportes.buscar_reportes(termino, rol, f_ini, f_fin)
        self.lbl_resultados.configure(text=f"Resultados: {len(resultados)}")
        
        for fila_datos in resultados:
            self.crear_fila(fila_datos)

    def crear_fila(self, datos):
        id_reporte = datos[-1] # El ID está al final
        datos_visuales = datos[:-1] # El resto son datos visuales

        row = ctk.CTkFrame(self.table_body, fg_color="transparent", height=45)
        row.pack(fill="x", pady=2)
        ctk.CTkFrame(row, height=1, fg_color="#E5E7EB").pack(side="bottom", fill="x")

        for i, dato in enumerate(datos_visuales):
            if i == 2: # Columna ROL con colores
                bg = "#E0E7FF" if dato == "Estudiante" else "#DCFCE7" if dato == "Docente" else "#F3F4F6"
                fg = "#3730A3" if dato == "Estudiante" else "#166534"
                lbl = ctk.CTkLabel(row, text=str(dato), font=("Arimo", 12), text_color=fg, fg_color=bg, corner_radius=5, width=self.widths[i])
                lbl.pack(side="left", padx=5)
            else:
                ctk.CTkLabel(row, text=str(dato), font=("Arimo", 13), text_color="#0A0A0A", anchor="w", width=self.widths[i]).pack(side="left", padx=5)
        
        # Botón VER con ID vinculado
        ctk.CTkButton(row, text="Ver", width=50, height=25, fg_color="#EFF6FF", text_color="#1D4ED8", hover_color="#DBEAFE", 
                      command=lambda id=id_reporte: self.ver_detalle(id)).pack(side="left", padx=5)

    def ver_detalle(self, id_reporte):
        datos = Consultas_reportes.obtener_detalle(id_reporte)
        if not datos: return

        img_blob, fecha, hora, tipo, placa, modelo, color, nombre, rol = datos
        
        # Ventana Emergente
        toplevel = ctk.CTkToplevel(self)
        toplevel.geometry("700x500")
        toplevel.title(f"Detalle Reporte #{id_reporte}")
        toplevel.configure(fg_color="white")
        toplevel.grab_set() # Bloquear ventana principal

        # 1. Imagen (Izquierda)
        img_frame = ctk.CTkFrame(toplevel, width=400, height=500, fg_color="#F3F4F6")
        img_frame.pack(side="left", fill="y")
        
        try:
            if img_blob:
                image_data = io.BytesIO(img_blob)
                pil_img = Image.open(image_data)
                ctk_img = ctk.CTkImage(light_image=pil_img, size=(380, 280))
                ctk.CTkLabel(img_frame, text="", image=ctk_img).place(relx=0.5, rely=0.5, anchor="center")
            else:
                ctk.CTkLabel(img_frame, text="Sin Imagen", text_color="gray").place(relx=0.5, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(img_frame, text="Error Imagen", text_color="red").place(relx=0.5, rely=0.5, anchor="center")

        # 2. Info (Derecha)
        info = ctk.CTkFrame(toplevel, fg_color="white")
        info.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        color_tipo = "#16A34A" if tipo == "Entrada" else "#DC2626"
        ctk.CTkLabel(info, text=f"● {tipo}", font=("Arial", 14, "bold"), text_color=color_tipo).pack(anchor="w")
        ctk.CTkLabel(info, text="Detalle de Acceso", font=("Arial", 20, "bold")).pack(anchor="w", pady=5)
        
        self.crear_dato_detalle(info, "Fecha:", f"{fecha} {hora}")
        self.crear_dato_detalle(info, "Conductor:", nombre)
        self.crear_dato_detalle(info, "Rol:", rol)
        ctk.CTkFrame(info, height=2, fg_color="#E5E7EB").pack(fill="x", pady=10)
        self.crear_dato_detalle(info, "Vehículo:", f"{modelo} {color}")
        self.crear_dato_detalle(info, "Placas:", placa)
        
        ctk.CTkButton(info, text="Cerrar", fg_color="black", command=toplevel.destroy).pack(side="bottom", fill="x")

    def crear_dato_detalle(self, parent, label, value):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=label, font=("Arial", 12, "bold"), text_color="gray", width=100, anchor="w").pack(side="left")
        ctk.CTkLabel(f, text=str(value), font=("Arial", 13), text_color="black").pack(side="left")

    def limpiar_filtros(self):
        self.entry_search.delete(0, 'end')
        self.entry_fecha_ini.delete(0, 'end')
        self.entry_fecha_fin.delete(0, 'end')
        self.cb_filtro_rol.set("Todos")
        self.realizar_busqueda(None)

    def volver(self):
        self.controller.show_frame(self.controller.vista_retorno)