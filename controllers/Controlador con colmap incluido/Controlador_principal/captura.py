import os
import cv2
import numpy as np

class CapturaImagenes:

    def __init__(self, camera):

        self.camera = camera

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.base_dir, "fotos_capturadas")

        os.makedirs(self.images_dir, exist_ok=True)

    def count_images(self):

        return len([
            f for f in os.listdir(self.images_dir)
            if f.lower().endswith((".jpg",".jpeg"))
        ])

    def save_image(self):

        image = self.camera.getImage()

        if image is None:
            return False

        width = self.camera.getWidth()
        height = self.camera.getHeight()

        img = np.frombuffer(
            image,
            dtype=np.uint8
        ).reshape((height,width,4))

        img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)

        filename = os.path.join(
            self.images_dir,
            f"foto_{self.count_images():04d}.jpg"
        )

        cv2.imwrite(
            filename,
            img,
            [cv2.IMWRITE_JPEG_QUALITY,95]
        )

        return True

    def limpiar(self):

        for archivo in os.listdir(self.images_dir):

            if archivo.lower().endswith((".jpg",".jpeg")):

                os.remove(
                    os.path.join(self.images_dir,archivo)
                )