import cv2
import numpy as np
import math
import os
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="models/yolov8s.pt", window_name="Drone camara"):
        # Asegurarnos de que exista la carpeta donde se va a descargar el modelo
        directorio = os.path.dirname(model_path)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
            
        self.model = YOLO(model_path)
        self.window_name = window_name
        self.clases_aceptadas = ["person", "bottle", "cup", "vase", "fire hydrant", "sports ball"]
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)

    def process_image(self, img_data, img_width, img_height, fov):
        if not img_data:
            return
            
        # Webots devuelve imagen en bytes formato BGRA
        img_np = np.frombuffer(img_data, np.uint8).reshape((img_height, img_width, 4))
        
        # Convertir a BGR para OpenCV
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
        
        # Inferencia YOLO (silenciada para no llenar la consola)
        results = self.model(img_bgr, verbose=False)
        
        for r in results:
            for box in r.boxes:
                # Coordenadas Bounding box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = round(float(box.conf[0]), 2)
                
                # Ignorar detecciones con baja confianza (menor al 50%)
                if conf < 0.5:
                    continue
                    
                cls = int(box.cls[0])
                class_name = self.model.names[cls]
                
                # Filtrar por clases (ignorar sillas, mesas, monitores, etc)
                if class_name not in self.clases_aceptadas:
                    continue
                
                # Dibujar bounding box
                cv2.rectangle(img_bgr, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Estimacion de tamaño y distancia
                bbox_height = float(y2 - y1)
                if bbox_height <= 0:
                    bbox_height = 1.0 # Prevenir division por cero
                
                # Alturas estimadas reales (metros)
                if class_name == "person":
                    real_height = 1.70 # Humano
                else:
                    real_height = 1.0 # Barril (YOLO suele detectarlo con otras etiquetas, no existe la etiqueta de barril)
                    
                # Calculo de distancia usando Pinhole model
                dist_estimada = (real_height * img_height) / (bbox_height * 2 * math.tan(fov/2))
                
                # Textos a mostrar
                label = f"{class_name} {conf}"
                dist_text = f"Dist: {dist_estimada:.2f}m"
                size_text = f"H_px: {int(bbox_height)}"
                
                cv2.putText(img_bgr, label, (int(x1), int(y1)-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(img_bgr, dist_text, (int(x1), int(y1)-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                cv2.putText(img_bgr, size_text, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                
        # Mostrar la ventana
        cv2.imshow(self.window_name, img_bgr)
        cv2.waitKey(1)
