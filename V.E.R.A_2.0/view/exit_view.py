import customtkinter as ctk
from PIL import Image
import os

class ExitView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="white")

        # Contenedor centrado
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Logo 
        try:
            ruta = os.path.join("view", "logo_integradora.png")
            img = ctk.CTkImage(Image.open(ruta), size=(180, 180))
            ctk.CTkLabel(self.center_frame, text="", image=img).pack(pady=(0, 20))
        except:
            ctk.CTkLabel(self.center_frame, text="LOGO V.E.R.A.", font=("Arial", 30, "bold")).pack(pady=(0, 20))


        # 2. Textos
        ctk.CTkLabel(self.center_frame, text="Cerrando Sistema", font=("Arial", 30, "bold"), text_color="#0F172B").pack()
        
        # 3. Barra
        self.progress_bar = ctk.CTkProgressBar(self.center_frame, width=400, height=15, corner_radius=10)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        self.progress_bar.configure(progress_color="#E7000B") # Rojo/Naranja para indicar cierre

        # 4. Estado
        self.lbl_status = ctk.CTkLabel(self.center_frame, text="Guardando cambios...", font=("Arial", 14), text_color="gray")
        self.lbl_status.pack()

        self.progreso = 0

    def iniciar_salida(self):
        """Inicia la animación de cierre"""
        self.progreso = 0
        self.animar()

    def animar(self):
        if self.progreso < 1.0:
            self.progreso += 0.02 # Velocidad de cierre
            self.progress_bar.set(self.progreso)
            
            # Cambiar textos para dar feedback al usuario
            if self.progreso > 0.3: self.lbl_status.configure(text="Respaldando base de datos...")
            if self.progreso > 0.6: self.lbl_status.configure(text="Cerrando conexiones seguras...")
            if self.progreso > 0.9: self.lbl_status.configure(text="Hasta luego.")

            self.after(20, self.animar)
        else:
            # --- AQUÍ SE CIERRA LA APP REALMENTE ---
            self.controller.destroy()