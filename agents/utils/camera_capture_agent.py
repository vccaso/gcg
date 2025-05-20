import cv2
from datetime import datetime
import os
import time

class CameraCaptureAgent:

    def run(self, device=0, save_path="workspace/camera/images", pic_name="image001.jpg"):
        os.makedirs(save_path, exist_ok=True)
        cap = cv2.VideoCapture(device)
        time.sleep(2) 
        if not cap.isOpened():
            return {"error": f"Cannot open camera device {device}"}

        ret, frame = cap.read()
        if not ret:
            return {
                "status": "Fail"
                "details" "Failed to capture image"
                }

        # Brightness enhancement (increase pixel values by 50)
        bright_frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=50)

        full_path = os.path.join(save_path, pic_name)
        cv2.imwrite(full_path, bright_frame)
        cap.release()  
        time.sleep(2)  
        return {"status": "Success", "details":full_path}

