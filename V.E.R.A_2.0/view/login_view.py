import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

class LoginView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.contrasena_es_visible = False
        # Usamos el mismo fondo gris claro de la app principal para que se fusione
        self.configure(fg_color="#F3F4F6") 

        # --- TARJETA CENTRAL BLANCA ---
        self.card = ctk.CTkFrame(self, fg_color="white", width=450, height=620, corner_radius=20)
        # Usamos place para centrarla matemáticamente en la ventana
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        # Evitamos que la tarjeta se encoja a sus hijos
        self.card.grid_propagate(False)
        self.card.pack_propagate(False)

        # =============================
        # 1. LOGO
        # =============================
        try:
            # Intenta cargar la imagen desde la carpeta view
            ruta = os.path.join("view", "logo_integradora.png")
            img = ctk.CTkImage(Image.open(ruta), size=(140, 140))
            ctk.CTkLabel(self.card, text="", image=img).pack(pady=(40, 10))
        except:
            # Texto de respaldo si falla la imagen
            ctk.CTkLabel(self.card, text="[LOGO V.E.R.A.]", font=("Arial", 20, "bold"), text_color="#0092B8").pack(pady=(40, 10))

        # =============================
        # 2. TÍTULOS
        # =============================
        ctk.CTkLabel(self.card, text="Bienvenido", font=("Arial", 28, "bold"), text_color="#0F172B").pack(pady=5)
        ctk.CTkLabel(self.card, text="Sistema de Vigilancia Élite\nde Reconocimiento de Acceso", font=("Arial", 15), text_color="#64748B", justify="center").pack(pady=(0, 30))

        # =============================
        # 3. INPUTS
        # =============================
        
        # --- Usuario / Correo ---
        ctk.CTkLabel(self.card, text="Correo electrónico", font=("Arial", 14, "bold"), text_color="#334155", anchor="w").pack(fill="x", padx=45, pady=(0, 5))
        
        self.entry_user = ctk.CTkEntry(
            self.card,
            placeholder_text="usuario@vera.security",
            height=45,
            font=("Arial", 14),
            border_color="#94A3B8", # Color de borde gris azulado
            border_width=2,
            corner_radius=8,
            fg_color="white",
            text_color="black"
        )
        self.entry_user.pack(fill="x", padx=45, pady=(0, 20))

        # --- Contraseña (CORREGIDO) ---
        # 1. Etiqueta (Forzamos color oscuro para que se vea)
        ctk.CTkLabel(self.card, text="Contraseña", font=("Arial", 14, "bold"), text_color="#334155", anchor="w").pack(fill="x", padx=45, pady=(0, 5))
        
        # 2. Marco Contenedor (Este es el que dibuja el borde)
        self.pass_frame = ctk.CTkFrame(
            self.card,
            height=45,
            fg_color="white",       # Fondo blanco
            border_color="#94A3B8", # Mismo color de borde que el correo
            border_width=2,         # Borde visible
            corner_radius=8
        )
        self.pass_frame.pack(fill="x", padx=45, pady=(0, 5))
        
        # 3. Entrada Transparente (Va adentro a la izquierda)
        self.entry_pass = ctk.CTkEntry(
            self.pass_frame,
            show="•",               # Ocultar texto
            height=40,
            border_width=0,         # SIN BORDE PROPIO
            fg_color="transparent", # FONDO TRANSPARENTE
            text_color="black",
            font=("Arial", 14),
            placeholder_text="••••••••"
        )
        # Usamos padding (padx) para que no se pegue al borde izquierdo del marco contenedor
        self.entry_pass.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=2)
        
        # 4. Botón del Ojo (Va adentro a la derecha)
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

        # =============================
        # 4. BOTÓN DE ACCIÓN
        # =============================
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
        """Alterna entre mostrar y ocultar la contraseña"""
        if self.contrasena_es_visible:
            self.entry_pass.configure(show="•") # Ocultar con punto
            self.btn_eye.configure(text="👁")   # Icono de ojo normal
            self.contrasena_es_visible = False
        else:
            self.entry_pass.configure(show="")  # Mostrar texto real
            self.btn_eye.configure(text="Ø")    # Icono de ojo tachado (simulado)
            self.contrasena_es_visible = True

    def validar(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        # --- CASO SUPER ADMIN (SUDOTE) ---
        if u == "sudote@vera.security" and p == "admin123":
            # 1. Guardamos la ruta de retorno
            self.controller.vista_retorno = "SudoteView"
            # 2. Cambiamos de pantalla
            self.controller.show_frame("SudoteView")
            self.limpiar()

        # --- CASO ADMIN LIMITADO (SUDITO) ---
        elif u == "sudito@vera.security" and p == "user123":
            # 1. Guardamos la ruta de retorno
            self.controller.vista_retorno = "SuditoView"
            # 2. Cambiamos de pantalla
            self.controller.show_frame("SuditoView")
            self.limpiar()

        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

        # --- RUTAS DE ACCESO ---
        if u == "sudote@vera.security" and p == "admin123":
            print("Acceso SUDOTE (Super Admin) concedido.")
            self.controller.show_frame("SudoteView")
            self.limpiar()

        elif u == "sudito@vera.security" and p == "user123":
            print("Acceso SUDITO (Admin Limitado) concedido.")
            self.controller.show_frame("SuditoView")
            self.limpiar()

        else:
            messagebox.showerror("Acceso Denegado", "Credenciales incorrectas.\nVerifique usuario y contraseña.")

    def limpiar(self):
        """Limpia los campos después de un login exitoso"""
        self.entry_user.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        # Reseteamos el ojo a oculto
        if self.contrasena_es_visible:
            self.toggle_pass()