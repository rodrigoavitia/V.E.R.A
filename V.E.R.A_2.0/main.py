import customtkinter as ctk
from view.login_view import LoginView
from view.sudote_view import SudoteView
from view.sudito_view import SuditoView
from view.registrar_vehiculo import RegistrarVehiculo
from view.registrar_usuario import RegistrarUsuario 
from view.reportes import ReportesView
from view.monitoreo_view import MonitoreoView

ctk.set_appearance_mode("Light")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema V.E.R.A.")
        self.geometry("1100x700")
        self.after(0, lambda: self.state('zoomed'))
        self.vista_retorno = "LoginView" 

        self.container = ctk.CTkFrame(self, fg_color="#F3F4F6")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # --- 2. AGREGAR AL BUCLE ---
        for F in (LoginView, SudoteView, SuditoView, RegistrarVehiculo, RegistrarUsuario, ReportesView, MonitoreoView):
            page_name = F.__name__
            frame = F(master=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        
        # --- TRUCO: Si es la pantalla de usuarios, actualiza los roles antes de mostrarla ---
        if page_name == "RegistrarUsuario":
            frame.configurar_roles()
            
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()