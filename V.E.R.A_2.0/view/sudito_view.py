import customtkinter as ctk
from tkinter import messagebox

class SuditoView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F8FAFC") 

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkLabel(header, text="Búfalos UTD", font=("Arial", 32, "bold"), text_color="#0F172B").pack(side="left")
        ctk.CTkButton(header, text="Cerrar Sesión", fg_color="#E7000B", height=40, command=self.logout).pack(side="right")

        # SUBHEADER
        sub = ctk.CTkFrame(self, fg_color="transparent")
        sub.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkFrame(sub, width=100, height=4, fg_color="#FFB900").pack(anchor="w", pady=(0,10))
        ctk.CTkLabel(sub, text="Selecciona una opción para continuar", font=("Arial", 16), text_color="#45556C").pack(anchor="w")
        
        # Etiqueta de Nivel
        ctk.CTkLabel(sub, text="👤 NIVEL: SUDITO (LIMITADO)", font=("Arial", 12, "bold"), text_color="#62748E").pack(anchor="w", pady=(5,0))

        # GRID TARJETAS
        self.grid_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_cards.pack(fill="both", expand=True, padx=40, pady=20)
        self.grid_cards.columnconfigure((0,1), weight=1)

        # --- TARJETA 1: VEHÍCULOS 
        self.add_card(0, 0, "Agregar Vehículo", "Registra un nuevo vehículo", "#0092B8", "#CEFAFE", "🚙",
                      comando=lambda: self.controller.show_frame("RegistrarVehiculo"))

        # --- TARJETA 2: REPORTES 
        self.add_card(0, 1, "Ver Reportes", "Consulta y genera reportes", "#E17100", "#FEF3C6", "📄",
                      comando=lambda: self.controller.show_frame("ReportesView"))

        # --- TARJETA 3: USUARIOS 
        self.add_card(1, 0, "Gestión de Usuarios", "Registra nuevos usuarios", "#7C3AED", "#EDE9FE", "👥",
                      comando=lambda: self.controller.show_frame("RegistrarUsuario"))

    def add_card(self, r, c, title, desc, color, bg, icon, comando):
        card = ctk.CTkFrame(self.grid_cards, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.grid(row=r, column=c, padx=15, pady=15, sticky="nsew") 
        
        icon_f = ctk.CTkFrame(card, width=50, height=50, fg_color=bg, corner_radius=12)
        icon_f.pack(anchor="w", padx=20, pady=20)
        ctk.CTkLabel(icon_f, text=icon, font=("Arial", 20), text_color=color).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=title, font=("Arial", 18, "bold"), text_color="black").pack(anchor="w", padx=20)
        ctk.CTkLabel(card, text=desc, font=("Arial", 13), text_color="gray").pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkButton(card, text="Seleccionar ➔", fg_color="transparent", text_color=color, anchor="w", font=("Arial", 14, "bold"), command=comando).pack(fill="x", padx=20, pady=20)

    def logout(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas salir?")
        if respuesta:
            self.controller.show_frame("LoginView")