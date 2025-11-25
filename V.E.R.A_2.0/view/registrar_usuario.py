import customtkinter as ctk
from tkinter import messagebox
import re 

class RegistrarUsuario(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F1F5F9")

        # --- TARJETA PRINCIPAL ---
        self.card = ctk.CTkFrame(self, fg_color="white", width=970, height=600, corner_radius=14)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)
        self.card.pack_propagate(False)

        # =================================================
        # PANEL IZQUIERDO 
        # =================================================
        self.left_panel = ctk.CTkFrame(self.card, width=280, height=600, corner_radius=14, fg_color="#7DD3C0")
        self.left_panel.place(x=0, y=0)
        
        # Color HEX sólido corregido (#A0E7E5)
        logo_box = ctk.CTkFrame(self.left_panel, width=60, height=60, fg_color="#A0E7E5", corner_radius=10)
        logo_box.place(x=32, y=200)
        ctk.CTkLabel(logo_box, text="👤", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.left_panel, text="Bienvenido", font=("Arial", 22, "bold"), text_color="white").place(x=32, y=280)
        ctk.CTkLabel(self.left_panel, text="Registra un nuevo miembro \n de la comunidad UTD.", font=("Arial", 14), text_color="#F0FDFA", justify="left").place(x=32, y=320)

        # =================================================
        # PANEL DERECHO (Formulario)
        # =================================================
        self.right_panel = ctk.CTkScrollableFrame(self.card, width=650, height=580, fg_color="transparent")
        self.right_panel.place(x=290, y=10)

        ctk.CTkLabel(self.right_panel, text="Crear cuenta", font=("Arial", 24, "bold"), text_color="#101828").pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(self.right_panel, text="Ingresa los datos personales del usuario", font=("Arial", 14), text_color="#64748B").pack(anchor="w", pady=(0, 20))

        # --- CAMPOS ---
        self.entry_nombre = self.crear_campo("Nombre(s) *", "Juan Carlos")
        self.entry_ape_pat = self.crear_campo("Apellido Paterno *", "García")
        self.entry_ape_mat = self.crear_campo("Apellido Materno *", "López")

        # --- ROLES ---
        ctk.CTkLabel(self.right_panel, text="Tipo de Usuario *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        
        self.cb_rol = ctk.CTkComboBox(
            self.right_panel, 
            height=40, 
            border_color="#D1D5DB", 
            fg_color="white", 
            text_color="black",
            dropdown_fg_color="white",
            button_color="#E5E7EB"
        )
        self.cb_rol.pack(fill="x", pady=(0, 5))
        
        # Configurar roles según permisos (Sudote vs Sudito)
        self.configurar_roles()

        self.entry_correo = self.crear_campo("Correo Electrónico *", "correo@ejemplo.com")

        # --- CONTRASEÑA ---
        ctk.CTkLabel(self.right_panel, text="Contraseña *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        
        self.entry_pass = ctk.CTkEntry(self.right_panel, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", show="•", placeholder_text="••••••••")
        self.entry_pass.pack(fill="x")
        self.entry_pass.bind("<KeyRelease>", self.actualizar_fuerza) # Actualiza barra al escribir

        self.progress_fuerza = ctk.CTkProgressBar(self.right_panel, height=6, width=100)
        self.progress_fuerza.set(0)
        self.progress_fuerza.pack(fill="x", pady=(5, 2))
        
        self.lbl_fuerza = ctk.CTkLabel(self.right_panel, text="Seguridad: Baja", font=("Arial", 10), text_color="gray")
        self.lbl_fuerza.pack(anchor="w")

        ctk.CTkLabel(self.right_panel, text="Confirmar Contraseña *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        self.entry_confirm = ctk.CTkEntry(self.right_panel, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", show="•")
        self.entry_confirm.pack(fill="x")

        # --- BOTONES ---
        btn_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        btn_frame.pack(fill="x", pady=40)

        self.btn_crear = ctk.CTkButton(
            btn_frame, 
            text="Crear cuenta", 
            fg_color="#7DD3C0", 
            hover_color="#5EBDA8",
            text_color="white",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.registrar
        )
        self.btn_crear.pack(fill="x", pady=(0, 10))

        self.btn_volver = ctk.CTkButton(
            btn_frame, 
            text="Volver a inicio", 
            fg_color="white", 
            text_color="#7DD3C0",
            border_color="#7DD3C0",
            border_width=2,
            hover_color="#F0FDFA",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.volver
        )
        self.btn_volver.pack(fill="x")

        # --- ACTIVAR NAVEGACIÓN CON ENTER ---
        self.setup_navigation()

    def crear_campo(self, titulo, placeholder):
        ctk.CTkLabel(self.right_panel, text=titulo, font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        entry = ctk.CTkEntry(self.right_panel, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", placeholder_text=placeholder)
        entry.pack(fill="x")
        return entry

    def configurar_roles(self):
        # Verifica desde dónde venimos para limitar las opciones
        origen = self.controller.vista_retorno 
        if origen == "SudoteView":
            # Sudote puede crear todo
            opciones = ["Sudito (Admin)", "Directivo", "Docente", "Estudiante", "Trabajador"]
        else:
            # Sudito NO puede crear admins
            opciones = ["Directivo", "Docente", "Estudiante", "Trabajador"]
        self.cb_rol.configure(values=opciones)
        self.cb_rol.set("Seleccionar...")

    def setup_navigation(self):
        """Configura la tecla ENTER para saltar entre campos"""
        # Lista ordenada de inputs (saltamos el ComboBox porque a veces atrapa el foco)
        widgets = [
            self.entry_nombre,
            self.entry_ape_pat,
            self.entry_ape_mat,
            self.entry_correo,
            self.entry_pass,
            self.entry_confirm
        ]
        
        # Enlazar cada uno con el siguiente
        for i in range(len(widgets) - 1):
            current = widgets[i]
            next_widget = widgets[i+1]
            current.bind("<Return>", lambda e, w=next_widget: w.focus())
            
        # El último campo ejecuta la acción de registrar
        self.entry_confirm.bind("<Return>", lambda e: self.registrar())

    def actualizar_fuerza(self, event):
        pwd = self.entry_pass.get()
        score = 0
        
        # Criterios de seguridad
        if len(pwd) >= 8: score += 1
        if re.search(r"[A-Z]", pwd): score += 1
        if re.search(r"[a-z]", pwd): score += 1
        if re.search(r"[0-9]", pwd): score += 1
        if re.search(r"[!@#$%^&*]", pwd): score += 1

        progreso = score / 5
        self.progress_fuerza.set(progreso)

        # Colores según seguridad
        if score <= 2:
            self.progress_fuerza.configure(progress_color="#EF4444")
            self.lbl_fuerza.configure(text="Seguridad: Débil", text_color="#EF4444")
        elif score == 3 or score == 4:
            self.progress_fuerza.configure(progress_color="#F59E0B")
            self.lbl_fuerza.configure(text="Seguridad: Media", text_color="#F59E0B")
        else:
            self.progress_fuerza.configure(progress_color="#10B981")
            self.lbl_fuerza.configure(text="Seguridad: Fuerte", text_color="#10B981")

    def registrar(self):
        # Validaciones
        if self.entry_pass.get() != self.entry_confirm.get():
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        rol = self.cb_rol.get()
        nombre = self.entry_nombre.get()
        
        if rol == "Seleccionar..." or not nombre:
            messagebox.showerror("Error", "Complete los campos obligatorios.")
            return

        messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado como '{rol}'.")
        self.limpiar()

    def limpiar(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_ape_pat.delete(0, 'end')
        self.entry_ape_mat.delete(0, 'end')
        self.entry_correo.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.entry_confirm.delete(0, 'end')
        self.progress_fuerza.set(0)
        self.lbl_fuerza.configure(text="Seguridad: Baja", text_color="gray")
        self.cb_rol.set("Seleccionar...")

    def volver(self):
        self.controller.show_frame(self.controller.vista_retorno)