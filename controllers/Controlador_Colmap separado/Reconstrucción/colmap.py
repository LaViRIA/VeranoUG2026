import os
import cv2
import shutil
import traceback
import subprocess
import numpy as np
from tkinter import Tk, filedialog

class Colmap_Control:

    def __init__(self, camera=None, colmap_exec=None, enable_dense=True):

        self.camera = camera
        self.enable_dense = enable_dense

        # Ocultar ventana principal de Tkinter
        root = Tk()
        root.withdraw()

        # Si no se proporcionó la ruta de COLMAP, pedirla al usuario
        if colmap_exec is None:
            print("Seleccione el ejecutable de COLMAP (colmap.exe)")
            colmap_exec = filedialog.askopenfilename(
                title="Seleccione colmap.exe",
                filetypes=[("COLMAP", "colmap.exe"), ("Executable", "*.exe")]
            )

        self.colmap_exec = colmap_exec

        # Seleccionar carpeta del proyecto
        print("Seleccione la carpeta donde se guardarán las imágenes y resultados")

        self.base_dir = filedialog.askdirectory(
            title="Seleccione la carpeta del proyecto"
        )

        if not self.base_dir:
            raise Exception("No se seleccionó ninguna carpeta.")

        self.base_dir = os.path.abspath(self.base_dir)

        self.images_dir = os.path.join(self.base_dir, "fotos_capturadas")
        self.output_dir = os.path.join(self.base_dir, "colmap_output")
        self.logs_dir = os.path.join(self.output_dir, "logs")
        self.sparse_dir = os.path.join(self.output_dir, "sparse")
        self.dense_dir = os.path.join(self.output_dir, "dense")
        self.database_path = os.path.join(self.output_dir, "database.db")

        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.sparse_dir, exist_ok=True)

    def _write_log(self,filename,text):
        os.makedirs(self.logs_dir,exist_ok=True)

        with open(
            os.path.join(self.logs_dir,filename),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(text)

    def count_images(self):
        if not os.path.exists(self.images_dir):
            return 0
        images = [f for f in os.listdir(self.images_dir) if f.lower().endswith((".jpg", ".jpeg"))]
        return len(images)

    def save_image(self):
        try:
            image = self.camera.getImage()
            if image is None:
                return False

            width = self.camera.getWidth()
            height = self.camera.getHeight()

            img = np.frombuffer(image,dtype=np.uint8).reshape((height,width,4))
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)

            idx = self.count_images()
            filename = os.path.join(self.images_dir,f"foto_{idx:04d}.jpg")

            cv2.imwrite(filename,img,[cv2.IMWRITE_JPEG_QUALITY,95])

            saved=cv2.imread(filename)

            return True

        except Exception:
            self._write_log("save_image_error.txt",traceback.format_exc())
            return False
    
    def reset_project(self):
        try:
            if os.path.exists(self.images_dir):
                shutil.rmtree(self.images_dir)

            if os.path.exists(self.output_dir):
                shutil.rmtree(self.output_dir)

            os.makedirs(self.images_dir,exist_ok=True)
            os.makedirs(self.output_dir,exist_ok=True)
            os.makedirs(self.logs_dir,exist_ok=True)
            os.makedirs(self.sparse_dir,exist_ok=True)
            os.makedirs(self.dense_dir,exist_ok=True)

        except Exception:
            print(traceback.format_exc())