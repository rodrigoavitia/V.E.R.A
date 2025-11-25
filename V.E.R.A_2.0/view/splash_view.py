import customtkinter as ctk
from PIL import Image
import os

class SplashView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="white") # Fondo blanco limpio

        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. LOGO
        try:
            ruta = os.path.join("view", "logo_integradora.png")
            img = ctk.CTkImage(Image.open(ruta), size=(180, 180))
            ctk.CTkLabel(self.center_frame, text="", image=img).pack(pady=(0, 20))
        except:
            ctk.CTkLabel(self.center_frame, text="LOGO V.E.R.A.", font=("Arial", 30, "bold")).pack(pady=(0, 20))

        # 2. TÍTULO
        ctk.CTkLabel(self.center_frame, text="V.E.R.A.", font=("Arial", 40, "bold"), text_color="#0F172B").pack()
        ctk.CTkLabel(self.center_frame, text="Sistema de Vigilancia Élite", font=("Arial", 16), text_color="gray").pack(pady=(5, 40))

        # 3. BARRA DE CARGA
        self.progress_bar = ctk.CTkProgressBar(self.center_frame, width=400, height=15, corner_radius=10)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0) # Iniciar en 0
        self.progress_bar.configure(progress_color="#0092B8") # Azul VERA

        # 4. TEXTO DE ESTADO
        self.lbl_status = ctk.CTkLabel(self.center_frame, text="Iniciando sistema...", font=("Arial", 12), text_color="gray")
        self.lbl_status.pack()

        # --- INICIAR ANIMACIÓN ---
        self.progreso_actual = 0
        self.iniciar_carga()

    def iniciar_carga(self):
        """Simula la carga del sistema"""
        if self.progreso_actual < 1.0:
            self.progreso_actual += 0.007  
            self.progress_bar.set(self.progreso_actual)
            
            # Texto dinámico
            if self.progreso_actual > 0.3: self.lbl_status.configure(text="Cargando módulos...")
            if self.progreso_actual > 0.6: self.lbl_status.configure(text="Conectando base de datos...")
            if self.progreso_actual > 0.9: self.lbl_status.configure(text="Finalizando...")

            
            self.after(30, self.iniciar_carga) 
        else:
            # Carga completa: Ir al Login
            self.controller.show_frame("LoginView")