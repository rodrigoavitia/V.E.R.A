import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
# IMPORTANTE: Importar el modelo
from model.usuarios import Consulta_usuarios 

class LoginView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.contrasena_es_visible = False
        self.configure(fg_color="#F3F4F6") 

        # ... (Todo tu código visual del __init__ se queda IGUAL) ...
        # Solo nos enfocamos en cambiar la lógica de abajo:

        # --- TARJETA CENTRAL BLANCA ---
        self.card = ctk.CTkFrame(self, fg_color="white", width=450, height=620, corner_radius=20)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)
        self.card.pack_propagate(False)

        # 1. LOGO
        try:
            ruta = os.path.join("view", "logo_integradora.png")
            img = ctk.CTkImage(Image.open(ruta), size=(140, 140))
            ctk.CTkLabel(self.card, text="", image=img).pack(pady=(40, 10))
        except:
            ctk.CTkLabel(self.card, text="[LOGO V.E.R.A.]", font=("Arial", 20, "bold"), text_color="#0092B8").pack(pady=(40, 10))

        # 2. TÍTULOS
        ctk.CTkLabel(self.card, text="Bienvenido", font=("Arial", 28, "bold"), text_color="#0F172B").pack(pady=5)
        ctk.CTkLabel(self.card, text="Sistema de Vigilancia Élite\nde Reconocimiento de Acceso", font=("Arial", 15), text_color="#64748B", justify="center").pack(pady=(0, 30))

        # 3. INPUTS
        ctk.CTkLabel(self.card, text="Correo electrónico", font=("Arial", 14, "bold"), text_color="#334155", anchor="w").pack(fill="x", padx=45, pady=(0, 5))
        
        self.entry_user = ctk.CTkEntry(
            self.card,
            placeholder_text="usuario@vera.security",
            height=45,
            font=("Arial", 14),
            border_color="#94A3B8",
            border_width=2,
            corner_radius=8,
            fg_color="white",
            text_color="black"
        )
        self.entry_user.pack(fill="x", padx=45, pady=(0, 20))

        ctk.CTkLabel(self.card, text="Contraseña", font=("Arial", 14, "bold"), text_color="#334155", anchor="w").pack(fill="x", padx=45, pady=(0, 5))
        
        self.pass_frame = ctk.CTkFrame(
            self.card,
            height=45,
            fg_color="white",
            border_color="#94A3B8",
            border_width=2,
            corner_radius=8
        )
        self.pass_frame.pack(fill="x", padx=45, pady=(0, 5))
        
        self.entry_pass = ctk.CTkEntry(
            self.pass_frame,
            show="•",
            height=40,
            border_width=0,
            fg_color="transparent",
            text_color="black",
            font=("Arial", 14),
            placeholder_text="••••••••"
        )
        self.entry_pass.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=2)
        
        self.btn_eye = ctk.CTkButton(
            self.pass_frame,
            text="👁",
            width=35,
            fg_color="transparent",
            text_color="#64748B",
            hover_color="#F1F5F9",
            font=("Arial", 18),
            command=self.toggle_pass
        )
        self.btn_eye.pack(side="right", padx=(0, 5), pady=2)

        # 4. BOTÓN DE ACCIÓN
        ctk.CTkButton(
            self.card, 
            text="Autorizar Acceso", 
            height=50, 
            fg_color="black", 
            text_color="white",
            hover_color="#333333",
            font=("Arial", 16, "bold"), 
            corner_radius=10,
            command=self.validar
        ).pack(fill="x", padx=45, pady=(30, 20))

    def toggle_pass(self):
        if self.contrasena_es_visible:
            self.entry_pass.configure(show="•")
            self.btn_eye.configure(text="👁")
            self.contrasena_es_visible = False
        else:
            self.entry_pass.configure(show="")
            self.btn_eye.configure(text="Ø")
            self.contrasena_es_visible = True

    def validar(self):
        """Valida credenciales contra la Base de Datos"""
        u = self.entry_user.get()
        p = self.entry_pass.get()

        # 1. BACKDOOR SUPER ADMIN (Siempre entra directo)
        if u == "sudote@vera.security" and p == "admin123":
            print("Acceso SUDOTE (Master) concedido.")
            self.controller.vista_retorno = "SudoteView"
            self.controller.show_frame("SudoteView")
            self.limpiar()
            return

        # 2. CONSULTAR BASE DE DATOS (Para Suditos y otros admins)
        datos_usuario = Consulta_usuarios.login(u, p)

        if datos_usuario:
            # datos_usuario es una tupla: (nombre, rol)
            nombre, rol = datos_usuario
            print(f"Acceso concedido a: {nombre} ({rol})")

            # Si es admin (cualquier nivel registrado en tabla admin), entra a SuditoView
            # (A menos que quieras diferenciar roles dentro de la tabla admin)
            self.controller.vista_retorno = "SuditoView"
            self.controller.show_frame("SuditoView")
            self.limpiar()
        else:
            messagebox.showerror("Acceso Denegado", "Credenciales incorrectas o usuario inactivo.")

    def limpiar(self):
        self.entry_user.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        if self.contrasena_es_visible:
            self.toggle_pass()