# view/monitoreo_view.py

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2 
import numpy as np

# IMPORTAR LÓGICA DE CONTROL
from model.vehiculos import Consultas_vehiculos 
from controller.ai_controller import LicensePlateDetector # <--- CLASE DE LA RN

class MonitoreoView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master) 
        self.controller = controller
        self.configure(fg_color="#F9FAFB")
        
        # --- 1. Inicialización de RECURSOS DE VIDEO Y ML ---
        # Definimos los atributos críticos aquí.
        self.detector = LicensePlateDetector(model_name='model/weights/best.pt') 
        self.video_source = "http://172.20.30.23:4747/video" 
        self.camera = cv2.VideoCapture(self.video_source)
        self.running = False
        
        # --- 2. Carga Segura de UI ---
        # La carga real de la UI debe hacerse después de que el objeto exista
        self.after(0, self.cargar_ui) 

    # ----------------------------------------------------
    # MÉTODOS DE BUCLE Y LÓGICA DE VIDEO
    # ----------------------------------------------------

    def update_video_feed(self):
        """
        Bucle principal: Llama a la detección, valida la BD y actualiza el display.
        """
        if not self.running: return

        # --- LÍNEA DE CAPTURA CORREGIDA ---
        # Captura el estado de retorno (ret) y el frame de la cámara
        ret, frame = self.camera.read() 
        # -----------------------------------

        if ret:
            # 1. EJECUTAR DETECCIÓN Y OBTENER RESULTADOS
            # Aquí se ejecuta YOLO/OpenCV
            annotated_frame, placa_detectada_str = self.detector.predict_frame(frame)
            
            # 2. VALIDACIÓN DB (Define es_autorizado)
            es_autorizado = False
            if placa_detectada_str and placa_detectada_str != 'None':
                # Verifica la placa en la base de datos
                es_autorizado = Consultas_vehiculos.verificar_placa_autorizada(placa_detectada_str)
            
            # 3. FEEDBACK VISUAL
            if es_autorizado:
                status_color = "#10B981" 
                mensaje = f"✅ AUTORIZADO: {placa_detectada_str}"
            elif placa_detectada_str:
                status_color = "#DC2626" 
                mensaje = f"❌ DENEGADO: {placa_detectada_str}"
            else:
                status_color = "gray"
                mensaje = "ESTADO: SIN DETECCIÓN"
                
            self.lbl_deteccion.configure(text=mensaje, text_color=status_color)

            # 4. ACTUALIZACIÓN DEL DISPLAY
            cv2_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv2_image)
            cam_img = ctk.CTkImage(light_image=pil_img, size=(780, 440))
            
            self.video_display.configure(image=cam_img, text="")
            self.video_display.image = cam_img 
            
            self.after(100, self.update_video_feed)
        else:
            self.after(1000, self.update_video_feed)

    def crear_badge(self, parent, text, text_color, bg_color, side="left"):
        """Helper para crear etiquetas de estado"""
        f = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=6)
        f.pack(side=side)
        ctk.CTkLabel(f, text=text, text_color=text_color, font=("Arial", 12, "bold")).pack(padx=8, pady=2)

    def volver(self):
        """Apaga la cámara y regresa al Dashboard."""
        self.running = False
        if self.camera.isOpened():
            self.camera.release()
        self.controller.show_frame("SudoteView")

    # ----------------------------------------------------
    # MÉTODOS DE INICIO Y CARGA DE UI (Deben ir al final)
    # ----------------------------------------------------
    
    def start_monitoring(self):
        """Se llama al final de la carga de UI para iniciar el bucle."""
        if self.camera.isOpened():
            self.running = True
            self.update_video_feed()
        else:
            messagebox.showerror("Error de Cámara", "No se pudo conectar al dispositivo de video (Webcam/IP).")
            self.video_display.configure(text="¡CÁMARA DESCONECTADA!", text_color="#DC2626")


    def cargar_ui(self):
        """Construye todos los widgets DEBE ser la última función definida."""
        
        # BANNER
        self.banner = ctk.CTkFrame(self, fg_color="#DC2626", height=40, corner_radius=0)
        self.banner.pack(fill="x", side="top")
        ctk.CTkLabel(self.banner, text="⚠️ WORK IN PROGRESS - MÓDULO DE CÁMARAS EN CONSTRUCCIÓN ⚠️", text_color="white", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # ENCABEZADO
        self.header = ctk.CTkFrame(self, fg_color="white", height=80, corner_radius=0)
        self.header.pack(fill="x", pady=(0, 20))
        # ... (Widgets de título, estado, y botón Volver) ...
        ctk.CTkButton(self.header, text="Volver", fg_color="white", command=self.volver).pack(side="right", padx=30)
        
        # CONTENIDO DIVIDIDO
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=0)
        self.content.columnconfigure(0, weight=3); self.content.columnconfigure(1, weight=1) 

        # PANEL IZQUIERDO: VIDEO FEED
        self.video_panel = ctk.CTkFrame(self.content, fg_color="white", corner_radius=14, border_color="#E5E7EB", border_width=1)
        self.video_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

        # Placeholder
        self.video_display = ctk.CTkLabel(self.video_panel, text="Esperando señal de cámara...", width=780, height=440, fg_color="#F3F4F6")
        self.video_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Etiqueta de Detección
        self.lbl_deteccion = ctk.CTkLabel(self.video_panel, text="ESTADO: SIN DETECCIÓN", font=("Arial", 18, "bold"), text_color="gray")
        self.lbl_deteccion.pack(pady=10)

        # Llamar al bucle
        self.start_monitoring()