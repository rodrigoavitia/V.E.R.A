import customtkinter as ctk
from tkinter import filedialog, messagebox

class RegistrarVehiculo(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Fondo general suave (según Figma #F9FAFB)
        self.configure(fg_color="#F9FAFB")

        # --- CONTENEDOR PRINCIPAL (Tarjeta Blanca Centrada) ---
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_color="#E5E7EB", border_width=1)
        self.main_card.pack(fill="both", expand=True, padx=40, pady=40)

        
        # 1. ENCABEZADO
        self.header = ctk.CTkFrame(self.main_card, fg_color="transparent", height=70)
        self.header.pack(fill="x")
        
        # Línea divisoria inferior del header
        linea = ctk.CTkFrame(self.header, height=2, fg_color="#F3F4F6")
        linea.pack(side="bottom", fill="x")

        ctk.CTkLabel(self.header, text="Registro de Vehículo", font=("Arial", 20, "bold"), text_color="#0A0A0A").pack(side="left", padx=30, pady=20)
        
        # Botón Volver (Estilo Menú)
        ctk.CTkButton(
            self.header, 
            text="Volver al Menú", 
            fg_color="white", 
            text_color="#0A0A0A", 
            border_color="#E5E7EB", 
            border_width=1,
            hover_color="#F3F4F6",
            width=100,
            command=self.volver_menu
        ).pack(side="right", padx=30)

        # ==========================
        # 2. CUERPO DEL FORMULARIO (Dos Columnas)
        # ==========================
        self.body = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=30, pady=20)
        self.body.columnconfigure(0, weight=1) # Columna Izq (Persona)
        self.body.columnconfigure(1, weight=1) # Columna Der (Vehículo)

        # --- COLUMNA IZQUIERDA: INFORMACIÓN PERSONA ---
        self.col_left = ctk.CTkFrame(self.body, fg_color="transparent")
        self.col_left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ctk.CTkLabel(self.col_left, text="Información de la Persona", font=("Arial", 14, "bold"), text_color="#0A0A0A", anchor="w").pack(fill="x", pady=(0, 15))

        # Campos Persona
        self.cb_tipo = self.crear_input(self.col_left, "Tipo *", widget_type="combo", values=["Estudiante", "Docente", "Administrativo", "Trabajador externo", "Trabajador"])
        self.entry_nombre = self.crear_input(self.col_left, "Nombre *", placeholder="Ingrese el nombre")
        self.entry_ape_pat = self.crear_input(self.col_left, "Apellido Paterno *", placeholder="Apellido paterno")
        self.entry_ape_mat = self.crear_input(self.col_left, "Apellido Materno *", placeholder="Apellido materno")
        self.entry_curp = self.crear_input(self.col_left, "CURP *", placeholder="AAAA000000HXXXXXX0")
        self.cb_estado = self.crear_input(self.col_left, "Estado *", widget_type="combo", values=["Durango", "Coahuila", "Sinaloa", "Otro"])

        # Área de Fotografía
        ctk.CTkLabel(self.col_left, text="Fotografía *", font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(10, 5))
        self.btn_foto = ctk.CTkButton(
            self.col_left, 
            text="Click para subir foto\no arrastra una imagen", 
            fg_color="white", 
            text_color="#6A7282", 
            border_color="#E5E7EB", 
            border_width=2, 
            border_spacing=10,
            height=80,
            hover_color="#F9FAFB",
            command=self.subir_foto
        )
        self.btn_foto.pack(fill="x")

        # --- COLUMNA DERECHA: INFORMACIÓN VEHÍCULO ---
        self.col_right = ctk.CTkFrame(self.body, fg_color="transparent")
        self.col_right.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        ctk.CTkLabel(self.col_right, text="Información del Vehículo", font=("Arial", 14, "bold"), text_color="#0A0A0A", anchor="w").pack(fill="x", pady=(0, 15))

        # Campos Vehículo
        self.entry_placas = self.crear_input(self.col_right, "Placas *", placeholder="ABC-1234")
        self.entry_marca = self.crear_input(self.col_right, "Marca *", placeholder="Toyota, Ford, etc.")
        self.entry_modelo = self.crear_input(self.col_right, "Modelo *", placeholder="Corolla, F-150, etc.")

        # Fila doble para Año y Color
        row_doble = ctk.CTkFrame(self.col_right, fg_color="transparent")
        row_doble.pack(fill="x", pady=5)
        
        # Frame izq (Año)
        f_anio = ctk.CTkFrame(row_doble, fg_color="transparent")
        f_anio.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_anio = self.crear_input(f_anio, "Año *", placeholder="2024")

        # Frame der (Color)
        f_color = ctk.CTkFrame(row_doble, fg_color="transparent")
        f_color.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.entry_color = self.crear_input(f_color, "Color *", placeholder="Blanco")

        # ==========================
        # 3. FOOTER (Botón Registrar)
        # ==========================
        self.footer = ctk.CTkFrame(self.main_card, fg_color="transparent", height=80)
        self.footer.pack(fill="x", side="bottom", padx=30, pady=30)
        
        linea_top = ctk.CTkFrame(self.footer, height=1, fg_color="#F3F4F6")
        linea_top.pack(side="top", fill="x", pady=(0, 20))

        self.btn_registrar = ctk.CTkButton(
            self.footer,
            text="Registrar",
            font=("Arial", 14, "bold"),
            fg_color="black",
            text_color="white",
            hover_color="#333333",
            height=40,
            width=150,
            command=self.registrar
        )
        self.btn_registrar.pack(side="right")

        # --- CONFIGURAR NAVEGACIÓN CON ENTER ---
        self.setup_navigation()

    def crear_input(self, parent, label_text, placeholder="", widget_type="entry", values=None):
        """Helper para crear inputs idénticos al diseño"""
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x", pady=(10, 2))
        
        if widget_type == "entry":
            widget = ctk.CTkEntry(
                parent, 
                placeholder_text=placeholder, 
                height=38, 
                border_color="#E5E7EB", 
                fg_color="white", 
                text_color="black"
            )
        elif widget_type == "combo":
            widget = ctk.CTkComboBox(
                parent, 
                values=values, 
                height=38, 
                border_color="#E5E7EB", 
                fg_color="white", 
                text_color="black",
                dropdown_fg_color="white",
                dropdown_text_color="black",
                button_color="#E5E7EB",
                button_hover_color="#D1D5DB"
            )
        
        widget.pack(fill="x")
        return widget

    def setup_navigation(self):
        """
        Vincula la tecla ENTER (<Return>) para saltar al siguiente campo.
        """
        # Lista ordenada de widgets por los que queremos navegar
        # Nota: Los ComboBox no siempre aceptan focus_set igual que los Entry, 
        # así que nos enfocamos en los Entrys principalmente.
        
        widgets = [
            self.entry_nombre,
            self.entry_ape_pat,
            self.entry_ape_mat,
            self.entry_curp,
            # (Aquí saltamos los combos y foto para ir a vehículo)
            self.entry_placas,
            self.entry_marca,
            self.entry_modelo,
            self.entry_anio,
            self.entry_color
        ]

        for i in range(len(widgets) - 1):
            current_widget = widgets[i]
            next_widget = widgets[i+1]
            
            # Al presionar Enter en el widget actual, pone el foco en el siguiente
            current_widget.bind("<Return>", lambda event, w=next_widget: w.focus())

        # El último widget (Color) dispara la función de registrar al dar Enter
        self.entry_color.bind("<Return>", lambda event: self.registrar())

    # --- ACCIONES ---
    def volver_menu(self):
        # Leemos la variable que guardamos en el Login
        vista_destino = self.controller.vista_retorno
        
        # Nos vamos a esa vista
        self.controller.show_frame(vista_destino)

    def subir_foto(self):
        filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.btn_foto.configure(text=f"Imagen seleccionada:\n{filepath.split('/')[-1]}")

    def registrar(self):
        # Aquí iría tu lógica de base de datos
        nombre = self.entry_nombre.get()
        placas = self.entry_placas.get()
        
        if nombre and placas:
            messagebox.showinfo("Éxito", f"Vehículo con placas {placas} registrado correctamente.")
            self.limpiar_form()
        else:
            messagebox.showerror("Error", "Por favor complete los campos obligatorios.")

    def limpiar_form(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_placas.delete(0, 'end')
        # ... limpiar el resto ...