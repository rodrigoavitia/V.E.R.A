import customtkinter as ctk
from tkinter import messagebox

class ReportesView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Fondo degradado simulado
        self.configure(fg_color="#F9FAFB")

        # --- CONTENEDOR PRINCIPAL ---
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=14, border_color="#E5E7EB", border_width=1)
        self.main_card.pack(fill="both", expand=True, padx=32, pady=32)

        # ==========================================
        # 🚨 BANNER "WORK IN PROGRESS" 🚨
        # ==========================================
        self.banner = ctk.CTkFrame(self.main_card, fg_color="#DC2626", height=50, corner_radius=0) # Rojo intenso
        self.banner.pack(fill="x", side="top")
        
        ctk.CTkLabel(
            self.banner, 
            text="⚠️ WORK IN PROGRESS - MÓDULO EN CONSTRUCCIÓN ⚠️", 
            text_color="white", 
            font=("Arial", 18, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        # ==========================
        # 1. ENCABEZADO
        # ==========================
        self.header = ctk.CTkFrame(self.main_card, fg_color="transparent", height=90)
        self.header.pack(fill="x", padx=24, pady=(10, 0)) # Ajusté el padding superior
        
        # Icono
        icon_box = ctk.CTkFrame(self.header, width=40, height=40, fg_color="transparent")
        icon_box.pack(side="left", anchor="n", pady=5)
        ctk.CTkLabel(icon_box, text="📄", font=("Arial", 24)).place(relx=0.5, rely=0.5, anchor="center")

        # Textos
        title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        title_frame.pack(side="left", padx=16)
        ctk.CTkLabel(title_frame, text="Sistema de Reportes - Estacionamiento Institucional", font=("Arimo", 24, "bold"), text_color="#0A0A0A").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Control y gestión de vehículos de estudiantes, trabajadores, administrativos y profesores", font=("Arimo", 14), text_color="#717182").pack(anchor="w")

        # Botón Volver
        ctk.CTkButton(self.header, text="Volver", fg_color="white", text_color="#0A0A0A", border_color="#E5E7EB", border_width=1, width=80, command=self.volver).pack(side="right", anchor="n")

        # Línea divisoria
        ctk.CTkFrame(self.main_card, height=2, fg_color="#F3F4F6").pack(fill="x", pady=24)

        # ==========================
        # 2. BARRA DE FILTROS (Deshabilitada visualmente si quieres, o funcional)
        # ==========================
        self.filters_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.filters_frame.pack(fill="x", padx=24)

        # Fila 1
        row1 = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 16))
        self.crear_filtro(row1, "Buscar por", "Nombre", width=200, side="left")
        self.entry_search = self.crear_filtro_input(row1, "Término de búsqueda", "Buscar...", width=400, side="left", icon="🔍")
        self.entry_search.bind("<Return>", self.realizar_busqueda)

        # Fila 2
        row2 = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 16))
        self.crear_filtro_combo(row2, "Tipo de usuario", "Todos")
        self.crear_filtro_combo(row2, "Tipo de reporte", "Todos", padx=20)
        self.crear_filtro_combo(row2, "Fecha desde", "Seleccionar fecha", padx=20)
        self.crear_filtro_combo(row2, "Fecha hasta", "Seleccionar fecha", padx=20)

        # Fila 3
        row3 = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 16))
        ctk.CTkButton(row3, text="⬇ Exportar", fg_color="white", text_color="#0A0A0A", border_color="#E5E7EB", border_width=1, width=100, hover_color="#F9FAFB").pack(side="left")
        ctk.CTkButton(row3, text="Limpiar filtros", fg_color="transparent", text_color="#0A0A0A", hover_color="#F3F4F6", width=100).pack(side="left", padx=10)

        # ==========================
        # 3. TABLA DE RESULTADOS
        # ==========================
        ctk.CTkLabel(self.main_card, text="Resultados (10)", font=("Arimo", 14, "bold"), text_color="#0A0A0A").pack(anchor="w", padx=24, pady=(10, 5))

        # Cabecera
        header_cols = ["Fecha", "Nombre", "Tipo", "Mat. Usuario", "Mat. Vehículo", "Espacio", "Entrada", "Salida", "Reporte", "Acciones"]
        widths = [100, 200, 120, 120, 120, 80, 80, 80, 100, 80]
        
        self.table_header = ctk.CTkFrame(self.main_card, fg_color="#F9FAFB", height=40, corner_radius=0)
        self.table_header.pack(fill="x", padx=24)
        
        for i, col in enumerate(header_cols):
            lbl = ctk.CTkLabel(self.table_header, text=col, font=("Arimo", 13, "bold"), text_color="#0A0A0A", anchor="w", width=widths[i])
            lbl.pack(side="left", padx=5)

        # Cuerpo
        self.table_body = ctk.CTkScrollableFrame(self.main_card, fg_color="transparent", height=400)
        self.table_body.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        # Datos Demo
        datos = [
            ("15/11/2025", "Juan Pérez", "Estudiante", "EST-2021", "ABC-123", "A-15", "08:30", "17:45", "Diario", "#030213"),
            ("15/11/2025", "María Gzz", "Profesor", "PROF-089", "XYZ-789", "P-05", "07:45", "16:30", "Mensual", "#ECEEF2"),
            ("14/11/2025", "Pedro Rmz", "Trabajador", "TRAB-055", "MNO-345", "T-05", "07:00", "15:00", "Semanal", "#ECEEF2"),
        ]

        for fila in datos:
            self.crear_fila(fila, widths)

    # --- HELPERS ---
    def crear_filtro(self, parent, label, value, width=150, side="left", padx=0):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side=side, padx=padx)
        ctk.CTkLabel(f, text=label, font=("Arimo", 14), text_color="#0A0A0A").pack(anchor="w")
        btn = ctk.CTkButton(f, text=value, fg_color="#F3F3F5", text_color="#0A0A0A", hover_color="#E5E7EB", width=width, anchor="w")
        btn.pack()
        return btn

    def crear_filtro_input(self, parent, label, placeholder, width=150, side="left", icon="", padx=20):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side=side, padx=padx)
        ctk.CTkLabel(f, text=label, font=("Arimo", 14), text_color="#0A0A0A").pack(anchor="w")
        entry = ctk.CTkEntry(f, placeholder_text=f"{icon} {placeholder}", width=width, fg_color="#F3F3F5", border_width=0, text_color="black")
        entry.pack()
        return entry

    def crear_filtro_combo(self, parent, label, value, padx=0):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(side="left", padx=padx)
        ctk.CTkLabel(f, text=label, font=("Arimo", 14), text_color="#0A0A0A").pack(anchor="w")
        combo = ctk.CTkComboBox(f, values=[value, "Opción A", "Opción B"], width=180, fg_color="#F3F3F5", border_width=0, text_color="black", button_color="#E5E7EB")
        combo.pack()

    def crear_fila(self, datos, widths):
        row = ctk.CTkFrame(self.table_body, fg_color="transparent", height=50)
        row.pack(fill="x", pady=2)
        ctk.CTkFrame(row, height=1, fg_color="#E5E7EB").pack(side="bottom", fill="x")

        for i, dato in enumerate(datos[:-1]): 
            if i == 2: 
                bg_color = datos[-1]
                text_color = "white" if bg_color == "#030213" else "#0A0A0A"
                lbl_frame = ctk.CTkFrame(row, fg_color=bg_color, width=widths[i]-20, height=25, corner_radius=6)
                lbl_frame.pack(side="left", padx=5)
                lbl_frame.pack_propagate(False)
                ctk.CTkLabel(lbl_frame, text=dato, font=("Arimo", 12), text_color=text_color).place(relx=0.5, rely=0.5, anchor="center")
            else:
                ctk.CTkLabel(row, text=dato, font=("Arimo", 13), text_color="#0A0A0A", anchor="w", width=widths[i]).pack(side="left", padx=5)
        
        ctk.CTkButton(row, text="...", width=30, fg_color="transparent", text_color="black", hover_color="#F3F3F5").pack(side="left", padx=10)

    def realizar_busqueda(self, event):
        messagebox.showinfo("Info", "Función en construcción")

    def volver(self):
        self.controller.show_frame(self.controller.vista_retorno)