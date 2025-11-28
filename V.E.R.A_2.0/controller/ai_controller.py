# controller/ai_controller.py

import cv2
import torch
import gc
import os
from PIL import Image
import numpy as np

os.environ['CUDA_LAUNCH_BLOCKING'] = '0'
torch.backends.cudnn.benchmark = True

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

class LicensePlateDetector:
    def __init__(self, model_name='model/weights/best.pt'):
        print("🚀 Inicializando detector...")
        
        # Configuración GPU
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if self.device == 'cuda':
            print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        
        # Cargar modelo YOLO
        self.model = self._load_yolo(model_name)
        
        # Cargar EasyOCR
        self.ocr_reader = self._load_easyocr()
        
        self.cap = None
        self.frame_count = 0
        
        print("✅ Detector listo")

    def _load_yolo(self, model_name):
        """Cargar modelo YOLO optimizado"""
        if not YOLO_AVAILABLE:
            raise ImportError("Ultralytics no instalado")
        
        try:
            model = YOLO(model_name)
            if self.device == 'cuda':
                model.to('cuda')
            print("✅ YOLO cargado")
            return model
        except Exception as e:
            print(f"❌ Error YOLO: {e}")
            raise

    def _load_easyocr(self):
        """Cargar EasyOCR con modelos"""
        if not EASYOCR_AVAILABLE:
            print("⚠️  EasyOCR no disponible")
            return None
        
        try:
            reader = easyocr.Reader(
                ['en'], 
                gpu=(self.device == 'cuda'),
                download_enabled=True,
                verbose=False
            )
            print("✅ EasyOCR cargado")
            return reader
        except Exception as e:
            print(f"⚠️  Error EasyOCR: {e}")
            return None

    def _clean_memory(self):
        """Limpieza eficiente de memoria"""
        if self.frame_count % 50 == 0:
            if self.device == 'cuda':
                torch.cuda.empty_cache()
            gc.collect()

    def _preprocess_plate(self, plate_img):
        """Preprocesamiento rápido para OCR"""
        try:
            # Redimensionar para consistencia
            h, w = plate_img.shape[:2]
            if w > 250:
                ratio = 250 / w
                new_size = (250, int(h * ratio))
                plate_img = cv2.resize(plate_img, new_size)
            
            # Mejorar contraste
            if len(plate_img.shape) == 3:
                gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
            else:
                gray = plate_img
            
            # Ecualización
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            return enhanced
        except:
            return plate_img

    def _validate_plate(self, text):
        """Validar formato de 7 caracteres"""
        if not text:
            return None
        
        clean = ''.join(c for c in text.upper() if c.isalnum())
        return clean if len(clean) == 7 else None

    def predict_frame(self, frame):
        """Procesamiento principal optimizado"""
        self.frame_count += 1
        self._clean_memory()
        
        plate_text = None
        result_frame = frame.copy()
        
        try:
            # Detección YOLO
            with torch.no_grad():
                results = self.model(
                    frame, 
                    conf=0.6,
                    iou=0.5,
                    verbose=False,
                    device=self.device
                )
            
            # Procesar detecciones
            if (results and results[0].boxes is not None and len(results[0].boxes) > 0):
                best_idx = results[0].boxes.conf.argmax()
                best_box = results[0].boxes[best_idx]
                
                if best_box.conf > 0.6:
                    x1, y1, x2, y2 = best_box.xyxy[0].cpu().numpy().astype(int)
                    
                    # Recortar placa
                    plate_crop = frame[y1:y2, x1:x2]
                    
                    if (plate_crop.size > 0 and plate_crop.shape[0] > 20 and plate_crop.shape[1] > 60):
                        # OCR si disponible
                        if self.ocr_reader is not None:
                            try:
                                processed = self._preprocess_plate(plate_crop)
                                ocr_results = self.ocr_reader.readtext(
                                    processed,
                                    allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                                    detail=0,
                                    batch_size=1,
                                    width_ths=0.7
                                )
                                
                                if ocr_results:
                                    raw_text = ''.join(ocr_results).replace(' ', '')
                                    plate_text = self._validate_plate(raw_text)
                                    if plate_text:
                                        print(f"🚗 PLACA: {plate_text}")
                            except Exception as e:
                                print(f"⚠️  OCR error: {e}")
                    
                    # Dibujar resultados
                    result_frame = results[0].plot()
                    
                    if plate_text:
                        cv2.putText(
                            result_frame,
                            plate_text,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2
                        )
        
        except Exception as e:
            print(f"❌ Processing error: {e}")
        
        return result_frame, plate_text

    def stop_camera(self):
        """Liberar recursos"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        
        if self.device == 'cuda':
            torch.cuda.empty_cache()
        
        gc.collect()
        print("🧹 Recursos liberados")