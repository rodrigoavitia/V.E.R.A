import customtkinter as ctk
from PIL import Image, ImageTk
import os

class MonitoreoView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F9FAFB")

        # --- CONTENEDOR PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="#F9FAFB", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # BANNER
        self.banner = ctk.CTkFrame(self.main_container, fg_color="#DC2626", height=40, corner_radius=0)
        self.banner.pack(fill="x", side="top")
        ctk.CTkLabel(self.banner, text="⚠️ WORK IN PROGRESS - MÓDULO DE CÁMARAS EN CONSTRUCCIÓN ⚠️", text_color="white", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # HEADER
        self.header = ctk.CTkFrame(self.main_container, fg_color="white", height=80, corner_radius=0)
        self.header.pack(fill="x", pady=(0, 20))
        ctk.CTkFrame(self.header, height=2, fg_color="#E5E7EB").pack(side="bottom", fill="x")

        title_box = ctk.CTkFrame(self.header, fg_color="transparent")
        title_box.pack(side="left", padx=30, pady=15)
        ctk.CTkLabel(title_box, text="Sistema de Control de Estacionamiento", font=("Arial", 20, "bold"), text_color="#101828").pack(anchor="w")
        ctk.CTkLabel(title_box, text="Reconocimiento Automático de Placas (ANPR)", font=("Arial", 14), text_color="#4A5565").pack(anchor="w")

        status_box = ctk.CTkFrame(self.header, fg_color="transparent")
        status_box.pack(side="left", padx=20)
        self.crear_badge(status_box, "● Sistema Activo", text_color="#00A63E", bg_color="transparent")

        ctk.CTkButton(self.header, text="Volver", fg_color="white", text_color="#0A0A0A", border_color="#E5E7EB", border_width=1, command=self.volver).pack(side="right", padx=30)

        # GRID
        self.content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=0)
        self.content.columnconfigure(0, weight=3) 
        self.content.columnconfigure(1, weight=1) 

        # ==========================================
        # PANEL IZQUIERDO: VIDEO FEED
        # ==========================================
        self.video_panel = ctk.CTkFrame(self.content, fg_color="white", corner_radius=14, border_color="#E5E7EB", border_width=1)
        self.video_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

        # Cabecera Video
        video_header = ctk.CTkFrame(self.video_panel, fg_color="transparent", height=40)
        video_header.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(video_header, text="📷 Cámara 01 - Entrada Principal", font=("Arial", 16, "bold"), text_color="#101828").pack(side="left")
        self.crear_badge(video_header, "● EN VIVO", text_color="#FB2C36", bg_color="#FEF2F2")

        # --- ÁREA DE IMAGEN (CÁMARA) ---
        # Intentamos cargar la imagen, si falla ponemos un cuadro gris
        self.feed_container = ctk.CTkFrame(self.video_panel, fg_color="#F3F4F6", corner_radius=10)
        self.feed_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        try:
            # Ruta de la imagen
            ruta_img = os.path.join("view", "camara_demo.jpg")
            pil_img = Image.open(ruta_img)
            
            # Ajustamos la imagen para que sea vea grande (Ej: 800x450 px)
            # Usamos CTkImage para alta calidad
            cam_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(800, 450))
            
            # Usamos un Label para mostrar la imagen
            self.video_display = ctk.CTkLabel(self.feed_container, text="", image=cam_img)
            self.video_display.place(relx=0.5, rely=0.5, anchor="center") # Centrada
            
            # IMPORTANTE: Usamos el video_display como padre de los overlays
            parent_widget = self.video_display 
            
        except Exception as e:
            print(f"No se encontró la imagen de cámara: {e}")
            ctk.CTkLabel(self.feed_container, text="Sin señal de video", text_color="gray").place(relx=0.5, rely=0.5, anchor="center")
            parent_widget = self.feed_container

        # --- OVERLAYS (Superpuestos en la imagen) ---
        
        # 1. Hora (Fondo oscuro sólido)
        overlay_time = ctk.CTkFrame(parent_widget, fg_color="#1F2937", corner_radius=4) 
        overlay_time.place(x=20, y=20)
        ctk.CTkLabel(overlay_time, text="17:51:36", text_color="white", font=("Courier", 14, "bold")).pack(padx=10, pady=5)

        # 2. Zona de Escaneo (Marco Amarillo)
        # Nota: place es relativo al padre (la imagen)
        scan_zone = ctk.CTkFrame(parent_widget, fg_color="transparent", border_color="#FDC700", border_width=3, width=250, height=120)
        # Ajustamos posición para que coincida con la placa del coche en la foto
        scan_zone.place(relx=0.35, rely=0.75, anchor="center") 
        ctk.CTkLabel(scan_zone, text="ZONA DE ESCANEO", text_color="#FDC700", font=("Arial", 10, "bold"), bg_color="#1F2937").place(relx=0.5, rely=0, anchor="n")

        # 3. Etiqueta "Escaneando"
        scanning_tag = ctk.CTkFrame(parent_widget, fg_color="white", corner_radius=8, border_color="#2B7FFF", border_width=1)
        scanning_tag.place(relx=0.95, rely=0.95, anchor="se") # Esquina inferior derecha
        ctk.CTkLabel(scanning_tag, text="Escaneando...", text_color="#155DFC", font=("Arial", 12, "bold")).pack(padx=15, pady=5)


        # ==========================================
        # PANEL DERECHO: SIDEBAR
        # ==========================================
        self.sidebar = ctk.CTkFrame(self.content, fg_color="white", corner_radius=14, border_color="#E5E7EB", border_width=1)
        self.sidebar.grid(row=0, column=1, sticky="nsew", pady=10)

        stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=20)
        
        self.crear_mini_stat(stats_frame, "Vehículos Hoy", "156", "#EFF6FF", "#1447E6") 
        self.crear_mini_stat(stats_frame, "Activos", "250", "#F0FDF4", "#008236")      
        self.crear_mini_stat(stats_frame, "Inactivos", "100", "#FEF2F2", "#C10007")      

        ctk.CTkLabel(self.sidebar, text="Última Detección", font=("Arial", 16, "bold"), text_color="#101828").pack(anchor="w", padx=20, pady=(10, 5))
        
        last_det = ctk.CTkFrame(self.sidebar, fg_color="white", border_color="#E5E7EB", border_width=1, corner_radius=10)
        last_det.pack(fill="x", padx=15, pady=10)
        
        plate_header = ctk.CTkFrame(last_det, fg_color="transparent")
        plate_header.pack(fill="x", padx=10, pady=10)
        
        plate_box = ctk.CTkFrame(plate_header, fg_color="#FDC700", corner_radius=4, border_color="black", border_width=2)
        plate_box.pack(side="left")
        ctk.CTkLabel(plate_box, text="1234 AB", font=("Courier", 20, "bold"), text_color="black").pack(padx=10, pady=5)
        
        self.crear_badge(plate_header, "ACTIVA", "#00C950", "#F0FDF4", side="right")

        self.crear_info_row(last_det, "Hora:", "17:51:36")
        self.crear_info_row(last_det, "Confianza:", "99.8%")

        ctk.CTkLabel(self.sidebar, text="Detecciones Recientes", font=("Arial", 14, "bold"), text_color="#4A5565").pack(anchor="w", padx=20, pady=(20, 5))
        
        recent_list = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", height=200)
        recent_list.pack(fill="both", expand=True, padx=10, pady=5)

        self.crear_item_reciente(recent_list, "1234 AB", "17:51:36", True)
        self.crear_item_reciente(recent_list, "XYZ-999", "17:48:10", True)
        self.crear_item_reciente(recent_list, "BAD-000", "17:40:05", False)

    # --- HELPERS ---
    def crear_badge(self, parent, text, text_color, bg_color, side="left"):
        f = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=6)
        f.pack(side=side)
        ctk.CTkLabel(f, text=text, text_color=text_color, font=("Arial", 12, "bold")).pack(padx=8, pady=2)

    def crear_mini_stat(self, parent, title, value, bg_color, text_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10)
        card.pack(fill="x", pady=5)
        ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color="#364153").pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkLabel(card, text=value, font=("Arial", 20, "bold"), text_color=text_color).pack(anchor="w", padx=10, pady=(0, 8))

    def crear_info_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row, text=label, font=("Arial", 12), text_color="gray").pack(side="left")
        ctk.CTkLabel(row, text=value, font=("Arial", 12, "bold"), text_color="black").pack(side="right")

    def crear_item_reciente(self, parent, placa, hora, autorizada):
        row = ctk.CTkFrame(parent, fg_color="white", border_color="#E5E7EB", border_width=1)
        row.pack(fill="x", pady=4)
        ctk.CTkLabel(row, text="🚗", font=("Arial", 16)).pack(side="left", padx=10)
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", padx=5)
        ctk.CTkLabel(info, text=placa, font=("Courier", 14, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(info, text=hora, font=("Arial", 10), text_color="gray").pack(anchor="w")
        icono = "✓" if autorizada else "✗"
        color = "#00C950" if autorizada else "#C10007"
        ctk.CTkLabel(row, text=icono, text_color=color, font=("Arial", 16, "bold")).pack(side="right", padx=15)

    def volver(self):
        self.controller.show_frame("SudoteView")