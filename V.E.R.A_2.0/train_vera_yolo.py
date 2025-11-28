import os
from controller.ai_controller import LicensePlateDetector 
from ultralytics import settings

# --- 1. CONFIGURACIÓN DEL ENTORNO ---
# settings.update({'runs_dir': './yolo_runs'}) 

# --- 2. DEFINIR PARÁMETROS DEL DATASET ---
# CORREGIDO: Usamos el nombre exacto de la carpeta descargada de Roboflow
DATASET_PATH = 'license-plate.v1i.yolov5pytorch/' 
DATA_YAML_PATH = os.path.join(DATASET_PATH, 'data.yaml')

# --- 3. PARÁMETROS DE ENTRENAMIENTO ---
# Valores que definiste (puedes ajustarlos si lo deseas)
EPOCHS = 100       
IMAGE_SIZE = 640   
BATCH_SIZE = 16    

if __name__ == "__main__":
    if not os.path.exists(DATA_YAML_PATH):
        print("\n❌ ERROR: Archivo data.yaml no encontrado.")
        print(f"Por favor, asegúrate de que la carpeta '{DATASET_PATH}' esté en la raíz del proyecto.")
        exit()

    try:
        # Cargar el modelo base
        detector = LicensePlateDetector(model_name='yolov8n.pt') 
        
        # Iniciar el entrenamiento
        print("✅ Configuración de datos verificada. Iniciando entrenamiento...")
        detector.train_model(
            data_path=DATA_YAML_PATH,
            epochs=EPOCHS,
            img_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE
        )
        
        print("\n✅ ENTRENAMIENTO FINALIZADO CON ÉXITO.")
        print("Busca tu modelo 'best.pt' en la carpeta 'runs/detect/train/weights/'")
        
    except Exception as e:
        print(f"\n❌ FALLO EL ENTRENAMIENTO: Asegúrate de que PyTorch esté instalado correctamente.")
        print(f"Detalles del Error: {e}")