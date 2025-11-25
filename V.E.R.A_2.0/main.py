import customtkinter as ctk

# --- IMPORTACIÓN DE TODAS LAS VISTAS ---
from view.login_view import LoginView
from view.sudote_view import SudoteView
from view.sudito_view import SuditoView
from view.registrar_vehiculo import RegistrarVehiculo
from view.registrar_usuario import RegistrarUsuario
from view.reportes import ReportesView
from view.monitoreo_view import MonitoreoView
from view.splash_view import SplashView
from view.exit_view import ExitView

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema V.E.R.A. | Control de Acceso")
        self.after(0, lambda: self.state('zoomed'))
        
        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)
        
        self.geometry("1100x700")
        self.minsize(900, 650)
        self.configure(fg_color="#F3F4F6")
        
        self.vista_retorno = "LoginView" 

        self.container = ctk.CTkFrame(self, fg_color="#F3F4F6")
        self.container.pack(side="top", fill="both", expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Lista de todas las pantallas
        lista_vistas = (
            SplashView,
            ExitView,
            LoginView, 
            SudoteView, 
            SuditoView, 
            RegistrarVehiculo, 
            RegistrarUsuario, 
            ReportesView, 
            MonitoreoView
        )

        for F in lista_vistas:
            page_name = F.__name__
            frame = F(master=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Inicia con Splash
        self.show_frame("SplashView")

    def show_frame(self, page_name):
        """Trae al frente la vista solicitada"""
        frame = self.frames[page_name]
        
        # --- CORRECCIÓN AQUÍ ---
        if page_name == "RegistrarUsuario":
            # Llamamos al método con el nombre NUEVO
            if hasattr(frame, 'configurar_rol_unico'):
                frame.configurar_rol_unico()
            # Por seguridad, si alguna vez volvemos al nombre viejo
            elif hasattr(frame, 'configurar_roles'):
                frame.configurar_roles()
            
        frame.tkraise()

    # Lógica de cierre con pantalla de carga
    def confirmar_cierre(self):
        from tkinter import messagebox # Import local para evitar conflictos circulares si los hubiera
        respuesta = messagebox.askyesno("Salir del Sistema", "¿Estás seguro de que deseas salir?\nSe guardarán los cambios pendientes.")
        
        if respuesta:
            frame_salida = self.frames["ExitView"]
            frame_salida.tkraise()
            frame_salida.iniciar_salida()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()