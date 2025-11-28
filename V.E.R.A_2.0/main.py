import customtkinter as ctk

# Importar TODAS las Vistas (Modelos/Controladores)
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
        self.after(0, lambda: self.state('zoomed')) # Maximizar
        self.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)
        
        self.vista_retorno = "LoginView" 
        
        self.container = ctk.CTkFrame(self, fg_color="#F3F4F6")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Lista de todas las pantallas a inicializar
        lista_vistas = (
            SplashView, ExitView, LoginView, SudoteView, SuditoView, 
            RegistrarVehiculo, RegistrarUsuario, ReportesView, MonitoreoView
        )

        for F in lista_vistas:
            page_name = F.__name__
            frame = F(master=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SplashView") # Arrancamos con el Splash

    def show_frame(self, page_name):
        """Trae al frente la vista solicitada y ejecuta hooks de inicialización."""
        frame = self.frames[page_name]
        
        # Hooks de Inicialización: Se ejecutan justo antes de mostrar la pantalla
        if page_name == "RegistrarUsuario":
            # Llamamos al método que configura las opciones de rol
            if hasattr(frame, 'configurar_roles'):
                frame.configurar_roles()
            elif hasattr(frame, 'configurar_rol_unico'):
                frame.configurar_rol_unico()
        
        # Si es el monitoreo, reiniciamos el bucle de video
        if page_name == "MonitoreoView" and hasattr(frame, 'start_monitoring'):
            frame.start_monitoring()

        frame.tkraise()

    def confirmar_cierre(self):
        from tkinter import messagebox
        respuesta = messagebox.askyesno("Salir del Sistema", "¿Estás seguro de que deseas salir?")
        
        if respuesta:
            # Aseguramos que la cámara se libere si está activa
            if "MonitoreoView" in self.frames and self.frames["MonitoreoView"].running:
                self.frames["MonitoreoView"].camera.release()
            
            frame_salida = self.frames["ExitView"]
            frame_salida.tkraise()
            frame_salida.iniciar_salida() # Inicia el guardado y apagado

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()