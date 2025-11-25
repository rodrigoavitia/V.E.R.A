import customtkinter as ctk
from tkinter import messagebox
import re
from model.usuarios import Consulta_usuarios 

class RegistrarUsuario(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F1F5F9")

        # --- TARJETA PRINCIPAL ---
        self.card = ctk.CTkFrame(self, fg_color="white", width=970, height=620, corner_radius=14)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False); self.card.pack_propagate(False)

        # Panel Izquierdo
        self.left_panel = ctk.CTkFrame(self.card, width=280, height=620, corner_radius=14, fg_color="#7DD3C0")
        self.left_panel.place(x=0, y=0)
        logo_box = ctk.CTkFrame(self.left_panel, width=60, height=60, fg_color="#A0E7E5", corner_radius=10)
        logo_box.place(x=32, y=200)
        ctk.CTkLabel(logo_box, text="👤", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(self.left_panel, text="Bienvenido", font=("Arial", 22, "bold"), text_color="white").place(x=32, y=280)
        ctk.CTkLabel(self.left_panel, text="Registra un nuevo miembro\nde la comunidad UTD.", font=("Arial", 14), text_color="#F0FDFA", justify="left").place(x=32, y=320)

        # Panel Derecho
        self.right_panel = ctk.CTkScrollableFrame(self.card, width=650, height=600, fg_color="transparent")
        self.right_panel.place(x=290, y=10)

        ctk.CTkLabel(self.right_panel, text="Crear cuenta", font=("Arial", 24, "bold"), text_color="#101828").pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(self.right_panel, text="Ingresa los datos personales", font=("Arial", 14), text_color="#64748B").pack(anchor="w", pady=(0, 20))

        # Campos
        self.entry_nombre = self.crear_campo("Nombre(s) *", "Juan Carlos")
        self.entry_ape_pat = self.crear_campo("Apellido Paterno *", "García")
        self.entry_ape_mat = self.crear_campo("Apellido Materno *", "López")

        # Estado
        ctk.CTkLabel(self.right_panel, text="Estado del Usuario", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        self.switch_estado = ctk.CTkSwitch(self.right_panel, text="Activo", font=("Arial", 14), onvalue=True, offvalue=False, progress_color="#10B981")
        self.switch_estado.select()
        self.switch_estado.pack(anchor="w", pady=(0, 10))

        # Roles
        ctk.CTkLabel(self.right_panel, text="Tipo de Usuario *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        self.cb_rol = ctk.CTkComboBox(self.right_panel, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", button_color="#E5E7EB", command=self.verificar_cambio_rol)
        self.cb_rol.pack(fill="x", pady=(0, 5))
        
        # Credenciales
        self.frame_credenciales = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        ctk.CTkLabel(self.frame_credenciales, text="Correo Electrónico *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        self.entry_correo = ctk.CTkEntry(self.frame_credenciales, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", placeholder_text="admin@vera.security")
        self.entry_correo.pack(fill="x")

        ctk.CTkLabel(self.frame_credenciales, text="Contraseña *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        self.entry_pass = ctk.CTkEntry(self.frame_credenciales, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", show="•")
        self.entry_pass.pack(fill="x")
        self.entry_pass.bind("<KeyRelease>", self.actualizar_fuerza)

        self.progress_fuerza = ctk.CTkProgressBar(self.frame_credenciales, height=6, width=100)
        self.progress_fuerza.set(0); self.progress_fuerza.pack(fill="x", pady=(5, 2))
        self.lbl_fuerza = ctk.CTkLabel(self.frame_credenciales, text="Seguridad: Baja", font=("Arial", 10), text_color="gray"); self.lbl_fuerza.pack(anchor="w")

        ctk.CTkLabel(self.frame_credenciales, text="Confirmar Contraseña *", font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        self.entry_confirm = ctk.CTkEntry(self.frame_credenciales, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", show="•")
        self.entry_confirm.pack(fill="x")

        # Botones
        btn_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        btn_frame.pack(fill="x", pady=40)
        self.btn_crear = ctk.CTkButton(btn_frame, text="Crear cuenta", fg_color="#7DD3C0", hover_color="#5EBDA8", text_color="white", font=("Arial", 14, "bold"), height=40, command=self.registrar)
        self.btn_crear.pack(fill="x", pady=(0, 10))
        self.btn_volver = ctk.CTkButton(btn_frame, text="Volver a inicio", fg_color="white", text_color="#7DD3C0", border_color="#7DD3C0", border_width=2, hover_color="#F0FDFA", font=("Arial", 14, "bold"), height=40, command=self.volver)
        self.btn_volver.pack(fill="x")

        # Configuración
        self.configurar_roles() 
        self.setup_navigation()

    # --- MÉTODOS ---
    def crear_campo(self, titulo, placeholder):
        ctk.CTkLabel(self.right_panel, text=titulo, font=("Arial", 12, "bold"), text_color="#334155").pack(anchor="w", pady=(10, 5))
        entry = ctk.CTkEntry(self.right_panel, height=40, border_color="#D1D5DB", fg_color="white", text_color="black", placeholder_text=placeholder)
        entry.pack(fill="x")
        return entry

    def configurar_roles(self):
        self.frame_credenciales.pack_forget()
        origen = self.controller.vista_retorno 
        if origen == "SudoteView":
            opciones = ["Sudito (Admin)", "Directivo", "Docente", "Estudiante", "Trabajador"]
        else:
            opciones = ["Directivo", "Docente", "Estudiante", "Trabajador"]
        self.cb_rol.configure(values=opciones)
        self.cb_rol.set("Seleccionar...")

    def verificar_cambio_rol(self, eleccion):
        if "Sudito" in eleccion:
            self.frame_credenciales.pack(fill="x", after=self.cb_rol, pady=10)
        else:
            self.frame_credenciales.pack_forget()

    def registrar(self):
        nombre = self.entry_nombre.get()
        ape_pat = self.entry_ape_pat.get()
        ape_mat = self.entry_ape_mat.get()
        rol = self.cb_rol.get()
        estado = self.switch_estado.get()
        
        email_final = ""
        pass_final = ""

        # Validaciones
        if rol == "Seleccionar..." or not nombre or not ape_pat:
            messagebox.showerror("Error", "Faltan campos obligatorios.")
            return

        if "Sudito" in rol:
            email_final = self.entry_correo.get()
            pass_final = self.entry_pass.get()
            confirm = self.entry_confirm.get()
            if not email_final or not pass_final:
                messagebox.showerror("Error", "El administrador requiere Correo y Contraseña.")
                return
            if pass_final != confirm:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
        
        # Registro en BD
        exito = Consulta_usuarios.registrar_persona(
            nombre, ape_pat, ape_mat, rol, estado, email_final, pass_final
        )

        if exito:
            msg_estado = "Activo" if estado else "Inactivo"
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Registro Exitoso", f"Usuario '{nombre}' registrado correctamente ({msg_estado}).")
            
            self.limpiar() # Limpia el formulario actual
            
            # --- LÓGICA DE REDIRECCIÓN INTELIGENTE ---
            # Si NO es un Sudito (es decir, es un usuario normal), probablemente quiera registrar su coche
            if "Sudito" not in rol:
                respuesta = messagebox.askyesno("Continuar", "¿Desea registrar un vehículo para este usuario ahora?")
                if respuesta:
                    self.controller.show_frame("RegistrarVehiculo")
            
            # Si ES un Sudito, nos quedamos aquí para registrar otro o salir manualmente

    def limpiar(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_ape_pat.delete(0, 'end')
        self.entry_ape_mat.delete(0, 'end')
        self.entry_correo.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.entry_confirm.delete(0, 'end')
        self.cb_rol.set("Seleccionar...")
        self.switch_estado.select()
        self.frame_credenciales.pack_forget()
        self.progress_fuerza.set(0)
        self.lbl_fuerza.configure(text="Seguridad: Baja", text_color="gray")

    def setup_navigation(self):
        self.entry_nombre.bind("<Return>", lambda e: self.entry_ape_pat.focus())
        self.entry_ape_pat.bind("<Return>", lambda e: self.entry_ape_mat.focus())

    def actualizar_fuerza(self, event):
        pwd = self.entry_pass.get()
        score = 0
        if len(pwd) >= 8: score += 1
        if re.search(r"[A-Z]", pwd): score += 1
        if re.search(r"[a-z]", pwd): score += 1
        if re.search(r"[0-9]", pwd): score += 1
        if re.search(r"[!@#$%^&*]", pwd): score += 1
        self.progress_fuerza.set(score / 5)
        if score <= 2: self.progress_fuerza.configure(progress_color="#EF4444"); self.lbl_fuerza.configure(text="Seguridad: Débil", text_color="#EF4444")
        elif score <= 4: self.progress_fuerza.configure(progress_color="#F59E0B"); self.lbl_fuerza.configure(text="Seguridad: Media", text_color="#F59E0B")
        else: self.progress_fuerza.configure(progress_color="#10B981"); self.lbl_fuerza.configure(text="Seguridad: Fuerte", text_color="#10B981")

    def volver(self):
        self.controller.show_frame(self.controller.vista_retorno)