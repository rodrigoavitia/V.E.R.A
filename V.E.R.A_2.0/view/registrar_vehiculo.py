import customtkinter as ctk
from tkinter import filedialog, messagebox
from model.vehiculos import Consultas_vehiculos

class RegistrarVehiculo(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F9FAFB")
        self.usuario_id_seleccionado = None

        # Datos de Marcas/Modelos
        self.datos_vehiculos = {
            "Toyota": ["Corolla", "Yaris", "Camry", "RAV4", "Hilux", "Tacoma"],
            "Ford": ["Fiesta", "Focus", "Mustang", "F-150", "Escape", "Explorer"],
            "Chevrolet": ["Spark", "Aveo", "Cruze", "Camaro", "Silverado", "Trax"],
            "Nissan": ["Versa", "Sentra", "Altima", "March", "Frontier", "Kicks"],
            "Volkswagen": ["Jetta", "Golf", "Vento", "Polo", "Tiguan", "Saveiro"],
            "Honda": ["Civic", "Accord", "CR-V", "HR-V", "City", "Fit"],
            "BMW": ["Serie 3", "Serie 1", "X1", "X3", "X5", "M4"],
            "Mercedes-Benz": ["Clase A", "Clase C", "CLA", "GLA", "GLC"],
            "Hyundai": ["Grand i10", "Accent", "Elantra", "Tucson", "Creta"],
            "Kia": ["Rio", "Forte", "Soul", "Sportage", "Seltos"],
            "Otro": ["Otro"]
        }
        self.lista_marcas = list(self.datos_vehiculos.keys())

        # --- UI ---
        self.main_card = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_color="#E5E7EB", border_width=1)
        self.main_card.pack(fill="both", expand=True, padx=40, pady=40)

        # Header
        self.header = ctk.CTkFrame(self.main_card, fg_color="transparent", height=70)
        self.header.pack(fill="x")
        ctk.CTkFrame(self.header, height=2, fg_color="#F3F4F6").pack(side="bottom", fill="x")
        ctk.CTkLabel(self.header, text="Registro de Vehículo", font=("Arial", 20, "bold"), text_color="#0A0A0A").pack(side="left", padx=30)
        ctk.CTkButton(self.header, text="Volver al Menú", fg_color="white", text_color="#0A0A0A", border_color="#E5E7EB", hover_color="#F3F4F6", width=100, command=self.volver_menu).pack(side="right", padx=30)

        # Body Grid
        self.body = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=30, pady=20)
        self.body.columnconfigure(0, weight=1); self.body.columnconfigure(1, weight=1)

        # --- COLUMNA IZQUIERDA (Buscador Autocompletado) ---
        self.col_left = ctk.CTkFrame(self.body, fg_color="transparent")
        self.col_left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ctk.CTkLabel(self.col_left, text="Propietario del Vehículo", font=("Arial", 14, "bold"), text_color="#0A0A0A").pack(fill="x", pady=(0, 15))
        
        # Buscador
        ctk.CTkLabel(self.col_left, text="Buscar por Nombre o Apellido:", font=("Arial", 12), text_color="#4A5565").pack(fill="x", pady=(5, 2))
        
        # Frame relativo para poder poner la lista flotante debajo
        self.search_container = ctk.CTkFrame(self.col_left, fg_color="transparent")
        self.search_container.pack(fill="x")
        
        self.entry_busqueda = ctk.CTkEntry(self.search_container, placeholder_text="Escribe para buscar...", height=38, border_color="#E5E7EB", fg_color="white", text_color="black")
        self.entry_busqueda.pack(fill="x")
        self.entry_busqueda.bind("<KeyRelease>", self.on_search_type) # Evento al escribir

        # Lista de Sugerencias (Oculta inicialmente)
        self.suggestions_frame = ctk.CTkScrollableFrame(self.col_left, height=0, fg_color="white", border_color="#E5E7EB", border_width=1)
        # No la empaquetamos aún

        # Info Seleccionado
        self.info_frame = ctk.CTkFrame(self.col_left, fg_color="#F3F4F6", corner_radius=8, border_color="#E5E7EB", border_width=1)
        self.info_frame.pack(fill="x", pady=20)
        self.lbl_info_nombre = ctk.CTkLabel(self.info_frame, text="Sin usuario seleccionado", font=("Arial", 14, "bold"), text_color="#6A7282")
        self.lbl_info_nombre.pack(pady=(15, 5))
        self.lbl_info_tipo = ctk.CTkLabel(self.info_frame, text="---", font=("Arial", 12), text_color="#6A7282")
        self.lbl_info_tipo.pack(pady=(0, 15))

        self.btn_foto = ctk.CTkButton(self.col_left, text="Click para subir foto", fg_color="white", text_color="#6A7282", border_color="#E5E7EB", border_width=2, height=60, command=self.subir_foto)
        self.btn_foto.pack(fill="x")

        # --- COLUMNA DERECHA (Vehículo) ---
        self.col_right = ctk.CTkFrame(self.body, fg_color="transparent")
        self.col_right.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        ctk.CTkLabel(self.col_right, text="Datos del Automóvil", font=("Arial", 14, "bold"), text_color="#0A0A0A").pack(fill="x", pady=(0, 15))
        
        self.entry_placas = self.crear_input(self.col_right, "Placas *", "ABC-1234")
        
        ctk.CTkLabel(self.col_right, text="Marca *", font=("Arial", 12), text_color="#4A5565").pack(fill="x")
        self.cb_marca = ctk.CTkComboBox(self.col_right, values=self.lista_marcas, height=38, fg_color="white", text_color="black", command=self.actualizar_modelos)
        self.cb_marca.pack(fill="x"); self.cb_marca.set("Seleccionar Marca")

        ctk.CTkLabel(self.col_right, text="Modelo *", font=("Arial", 12), text_color="#4A5565").pack(fill="x", pady=(10,0))
        self.cb_modelo = ctk.CTkComboBox(self.col_right, values=[], height=38, fg_color="white", text_color="black")
        self.cb_modelo.pack(fill="x"); self.cb_modelo.set("")

        row_doble = ctk.CTkFrame(self.col_right, fg_color="transparent")
        row_doble.pack(fill="x", pady=10)
        f1 = ctk.CTkFrame(row_doble, fg_color="transparent"); f1.pack(side="left", fill="x", expand=True)
        self.entry_anio = self.crear_input(f1, "Año *", "2024")
        f2 = ctk.CTkFrame(row_doble, fg_color="transparent"); f2.pack(side="right", fill="x", expand=True, padx=(10,0))
        self.entry_color = self.crear_input(f2, "Color *", "Blanco")

        # Footer
        self.footer = ctk.CTkFrame(self.main_card, fg_color="transparent", height=80)
        self.footer.pack(fill="x", side="bottom", padx=30, pady=30)
        ctk.CTkButton(self.footer, text="Registrar Vehículo", font=("Arial", 14, "bold"), fg_color="black", text_color="white", height=40, width=180, command=self.registrar).pack(side="right")

    # --- LÓGICA AUTOCOMPLETADO ---
    def on_search_type(self, event):
        termino = self.entry_busqueda.get()
        
        # Limpiar sugerencias anteriores
        for widget in self.suggestions_frame.winfo_children():
            widget.destroy()
        
        if len(termino) < 2: # Solo buscar si hay al menos 2 letras
            self.suggestions_frame.pack_forget()
            return

        # Consultar BD
        resultados = Consultas_vehiculos.buscar_usuarios_like(termino)
        
        if resultados:
            self.suggestions_frame.pack(fill="x", after=self.search_container, pady=2)
            self.suggestions_frame.configure(height=min(len(resultados)*40, 150)) # Ajustar altura
            
            for usuario in resultados:
                uid, nombre, pat, mat, tipo = usuario
                texto = f"{nombre} {pat} {mat} ({tipo})"
                btn = ctk.CTkButton(
                    self.suggestions_frame, 
                    text=texto, 
                    anchor="w", 
                    fg_color="transparent", 
                    text_color="black", 
                    hover_color="#E5E7EB",
                    command=lambda u=usuario: self.seleccionar_usuario(u)
                )
                btn.pack(fill="x", pady=1)
        else:
            self.suggestions_frame.pack_forget()

    def seleccionar_usuario(self, usuario_data):
        uid, nombre, pat, mat, tipo = usuario_data
        self.usuario_id_seleccionado = uid
        
        # Llenar UI
        self.entry_busqueda.delete(0, 'end')
        self.entry_busqueda.insert(0, f"{nombre} {pat}")
        self.lbl_info_nombre.configure(text=f"{nombre} {pat} {mat}", text_color="#0A0A0A")
        self.lbl_info_tipo.configure(text=f"Rol: {tipo} | ID: {uid}")
        self.info_frame.configure(fg_color="#F0FDF4", border_color="#10B981")
        
        # Ocultar sugerencias
        self.suggestions_frame.pack_forget()
        self.entry_placas.focus()

    # --- RESTO DE MÉTODOS (Igual que antes) ---
    def crear_input(self, parent, label_text, placeholder):
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="#4A5565", anchor="w").pack(fill="x")
        widget = ctk.CTkEntry(parent, placeholder_text=placeholder, height=38, border_color="#E5E7EB", fg_color="white", text_color="black")
        widget.pack(fill="x")
        return widget

    def actualizar_modelos(self, marca):
        if marca in self.datos_vehiculos:
            self.cb_modelo.configure(values=self.datos_vehiculos[marca])
            self.cb_modelo.set("Seleccionar Modelo")

    def registrar(self):
        if not self.usuario_id_seleccionado:
            messagebox.showerror("Error", "Seleccione un propietario.")
            return
        # (Lógica de registro igual a tu archivo anterior)
        Consultas_vehiculos.registrar_vehiculo(
            self.cb_marca.get(), self.cb_modelo.get(), self.entry_color.get(),
            self.entry_placas.get(), self.entry_anio.get(), self.usuario_id_seleccionado
        )
        messagebox.showinfo("Éxito", "Vehículo registrado")
        self.limpiar_form()

    def limpiar_form(self):
        self.usuario_id_seleccionado = None
        self.entry_busqueda.delete(0, 'end')
        self.lbl_info_nombre.configure(text="Sin usuario seleccionado", text_color="#6A7282")
        self.lbl_info_tipo.configure(text="---")
        self.info_frame.configure(fg_color="#F3F4F6", border_color="#E5E7EB")
        self.entry_placas.delete(0, 'end')
        self.entry_anio.delete(0, 'end')
        self.entry_color.delete(0, 'end')

    def volver_menu(self):
        self.controller.show_frame(self.controller.vista_retorno)

    def subir_foto(self):
        file = filedialog.askopenfilename()
        if file: self.btn_foto.configure(text="Imagen Cargada")