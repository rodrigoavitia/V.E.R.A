import customtkinter as ctk
from tkinter import filedialog, messagebox
from model.vehiculos import Consultas_vehiculos

class RegistrarVehiculo(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F9FAFB")
        self.usuario_id_seleccionado = None

        # --- DICCIONARIO DE DATOS (Marcas y Modelos) ---
        self.datos_vehiculos = {
            "Toyota": ["Corolla", "Yaris", "Camry", "RAV4", "Hilux", "Tacoma", "Otro"],
            "Ford": ["Fiesta", "Focus", "Mustang", "F-150", "Escape", "Explorer", "Otro"],
            "Chevrolet": ["Spark", "Aveo", "Cruze", "Camaro", "Silverado", "Trax", "Otro"],
            "Nissan": ["Versa", "Sentra", "Altima", "March", "Frontier", "Kicks", "Otro"],
            "Volkswagen": ["Jetta", "Golf", "Vento", "Polo", "Tiguan", "Saveiro", "Otro"],
            "Honda": ["Civic", "Accord", "CR-V", "HR-V", "City", "Fit", "Otro"],
            "BMW": ["Serie 3", "Serie 1", "X1", "X3", "X5", "M4", "Otro"],
            "Mercedes-Benz": ["Clase A", "Clase C", "CLA", "GLA", "GLC", "Otro"],
            "Hyundai": ["Grand i10", "Accent", "Elantra", "Tucson", "Creta", "Otro"],
            "Kia": ["Rio", "Forte", "Soul", "Sportage", "Seltos", "Otro"],
            "Otro": ["Otro"]    
        }
        self.lista_marcas = list(self.datos_vehiculos.keys())

        # --- CONTENEDOR PRINCIPAL ---
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_color="#E5E7EB", border_width=1)
        self.main_card.pack(fill="both", expand=True, padx=40, pady=40)

        # 1. ENCABEZADO
        self.header = ctk.CTkFrame(self.main_card, fg_color="transparent", height=70)
        self.header.pack(fill="x")
        ctk.CTkFrame(self.header, height=2, fg_color="#F3F4F6").pack(side="bottom", fill="x")
        ctk.CTkLabel(self.header, text="Registro de Vehículo", font=("Arial", 20, "bold"), text_color="#0A0A0A").pack(side="left", padx=30, pady=20)
        ctk.CTkButton(self.header, text="Volver al Menú", fg_color="white", text_color="#0A0A0A", border_color="#E5E7EB", border_width=1, hover_color="#F3F4F6", width=100, command=self.volver_menu).pack(side="right", padx=30)

        # 2. CUERPO
        self.body = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=30, pady=20)
        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=1)

        # --- COLUMNA IZQUIERDA: BUSCADOR ---
        self.col_left = ctk.CTkFrame(self.body, fg_color="transparent")
        self.col_left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ctk.CTkLabel(self.col_left, text="Propietario del Vehículo", font=("Arial", 14, "bold"), text_color="#0A0A0A", anchor="w").pack(fill="x", pady=(0, 15))
        
        # Buscador
        ctk.CTkLabel(self.col_left, text="Buscar por Nombre o Apellido:", font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(5, 2))
        search_frame = ctk.CTkFrame(self.col_left, fg_color="transparent")
        search_frame.pack(fill="x")
        self.entry_busqueda = ctk.CTkEntry(search_frame, placeholder_text="Ej. Juan Perez", height=38, border_color="#E5E7EB", fg_color="white", text_color="black")
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(search_frame, text="🔍 Buscar", width=80, height=38, fg_color="#0092B8", hover_color="#007AA3", command=self.buscar_usuario).pack(side="right")
        self.entry_busqueda.bind("<Return>", lambda e: self.buscar_usuario())

        # Info Usuario
        self.info_frame = ctk.CTkFrame(self.col_left, fg_color="#F3F4F6", corner_radius=8, border_color="#E5E7EB", border_width=1)
        self.info_frame.pack(fill="x", pady=20)
        self.lbl_info_nombre = ctk.CTkLabel(self.info_frame, text="Sin usuario seleccionado", font=("Arial", 14, "bold"), text_color="#6A7282")
        self.lbl_info_nombre.pack(pady=(15, 5), padx=15, anchor="w")
        self.lbl_info_tipo = ctk.CTkLabel(self.info_frame, text="---", font=("Arial", 12), text_color="#6A7282")
        self.lbl_info_tipo.pack(pady=(0, 15), padx=15, anchor="w")

        # Foto
        ctk.CTkLabel(self.col_left, text="Fotografía del Vehículo (Opcional)", font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(10, 5))
        self.btn_foto = ctk.CTkButton(self.col_left, text="Click para subir foto", fg_color="white", text_color="#6A7282", border_color="#E5E7EB", border_width=2, height=60, hover_color="#F9FAFB", command=self.subir_foto)
        self.btn_foto.pack(fill="x")

        # --- COLUMNA DERECHA: DATOS VEHÍCULO ---
        self.col_right = ctk.CTkFrame(self.body, fg_color="transparent")
        self.col_right.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        ctk.CTkLabel(self.col_right, text="Datos del Automóvil", font=("Arial", 14, "bold"), text_color="#0A0A0A", anchor="w").pack(fill="x", pady=(0, 15))

        # Placas
        self.entry_placas = self.crear_input(self.col_right, "Placas *", placeholder="ABC-1234")

        # --- MARCAS Y MODELOS DINÁMICOS ---
        # Marca
        ctk.CTkLabel(self.col_right, text="Marca *", font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(10, 2))
        self.cb_marca = ctk.CTkComboBox(
            self.col_right, 
            values=self.lista_marcas,
            height=38,
            border_color="#E5E7EB",
            fg_color="white",
            text_color="black",
            dropdown_fg_color="white",
            button_color="#E5E7EB",
            command=self.actualizar_modelos # <--- Evento al cambiar
        )
        self.cb_marca.pack(fill="x")
        self.cb_marca.set("Seleccionar Marca")

        # Modelo
        ctk.CTkLabel(self.col_right, text="Modelo *", font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(10, 2))
        self.cb_modelo = ctk.CTkComboBox(
            self.col_right, 
            values=["Seleccione una marca primero"],
            height=38,
            border_color="#E5E7EB",
            fg_color="white",
            text_color="black",
            dropdown_fg_color="white",
            button_color="#E5E7EB"
        )
        self.cb_modelo.pack(fill="x")
        self.cb_modelo.set("Seleccionar Modelo")

        # Año y Color
        row_doble = ctk.CTkFrame(self.col_right, fg_color="transparent")
        row_doble.pack(fill="x", pady=5)
        f_anio = ctk.CTkFrame(row_doble, fg_color="transparent"); f_anio.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_anio = self.crear_input(f_anio, "Año *", placeholder="2024")
        f_color = ctk.CTkFrame(row_doble, fg_color="transparent"); f_color.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.entry_color = self.crear_input(f_color, "Color *", placeholder="Blanco")

        # Footer
        self.footer = ctk.CTkFrame(self.main_card, fg_color="transparent", height=80)
        self.footer.pack(fill="x", side="bottom", padx=30, pady=30)
        ctk.CTkFrame(self.footer, height=1, fg_color="#F3F4F6").pack(side="top", fill="x", pady=(0, 20))
        ctk.CTkButton(self.footer, text="Registrar Vehículo", font=("Arial", 14, "bold"), fg_color="black", text_color="white", hover_color="#333333", height=40, width=180, command=self.registrar).pack(side="right")

    # --- MÉTODOS ---

    def actualizar_modelos(self, marca_seleccionada):
        """Actualiza el combo de modelos según la marca"""
        if marca_seleccionada in self.datos_vehiculos:
            modelos = self.datos_vehiculos[marca_seleccionada]
            self.cb_modelo.configure(values=modelos)
            self.cb_modelo.set("Seleccionar Modelo")
        else:
            self.cb_modelo.configure(values=[])
            self.cb_modelo.set("")

    def buscar_usuario(self):
        termino = self.entry_busqueda.get()
        if not termino: return
        
        datos_usuario = Consultas_vehiculos.buscar_propietario(termino)
        
        if datos_usuario:
            uid, nombre, pat, mat, tipo = datos_usuario
            self.usuario_id_seleccionado = uid
            self.lbl_info_nombre.configure(text=f"{nombre} {pat} {mat}", text_color="#0A0A0A")
            self.lbl_info_tipo.configure(text=f"Rol: {tipo} | ID: {uid}")
            self.info_frame.configure(fg_color="#F0FDF4", border_color="#10B981")
            self.entry_placas.focus()
        else:
            self.usuario_id_seleccionado = None
            self.lbl_info_nombre.configure(text="Usuario no encontrado", text_color="#EF4444")
            self.lbl_info_tipo.configure(text="Intente de nuevo")
            self.info_frame.configure(fg_color="#FEF2F2", border_color="#EF4444")

    def registrar(self):
        if self.usuario_id_seleccionado is None:
            messagebox.showerror("Error", "Seleccione un propietario.")
            return

        placas = self.entry_placas.get()
        marca = self.cb_marca.get() # Ahora es Combo
        modelo = self.cb_modelo.get() # Ahora es Combo
        anio = self.entry_anio.get()
        color = self.entry_color.get()

        if not placas or marca == "Seleccionar Marca" or modelo == "Seleccionar Modelo":
            messagebox.showerror("Error", "Complete los campos obligatorios.")
            return

        exito = Consultas_vehiculos.registrar_vehiculo(marca, modelo, color, placas, anio, self.usuario_id_seleccionado)
        if exito:
            messagebox.showinfo("Éxito", f"Vehículo {placas} registrado.")
            self.limpiar_form()

    def crear_input(self, parent, label_text, placeholder="", widget_type="entry", values=None):
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(10, 2))
        widget = ctk.CTkEntry(parent, placeholder_text=placeholder, height=38, border_color="#E5E7EB", fg_color="white", text_color="black")
        widget.pack(fill="x")
        return widget

    def limpiar_form(self):
        self.usuario_id_seleccionado = None
        self.entry_busqueda.delete(0, 'end')
        self.lbl_info_nombre.configure(text="Sin usuario seleccionado", text_color="#6A7282")
        self.lbl_info_tipo.configure(text="---")
        self.info_frame.configure(fg_color="#F3F4F6", border_color="#E5E7EB")
        self.entry_placas.delete(0, 'end')
        self.entry_anio.delete(0, 'end')
        self.entry_color.delete(0, 'end')
        self.cb_marca.set("Seleccionar Marca")
        self.cb_modelo.set("Seleccionar Modelo")

    def volver_menu(self):
        self.controller.show_frame(self.controller.vista_retorno)

    def subir_foto(self):
        file = filedialog.askopenfilename()
        if file: self.btn_foto.configure(text="Imagen Cargada")