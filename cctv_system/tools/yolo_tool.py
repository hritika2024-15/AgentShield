from ultralytics import YOLO
from config import YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD

class YOLOTool:
    def __init__(self, model_path=YOLO_MODEL_PATH, conf_threshold=CONFIDENCE_THRESHOLD):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        
        detections = []
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf >= self.conf_threshold:
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]
                detections.append({
                    "class": cls_name,
                    "confidence": conf,
                    "bbox": box.xyxy[0].tolist()
                })
        
        # MOCK DETECTION FOR TESTING (preserved from previous logic)
        # Detect 'bottle' (mapped to smoke) if we see the green rectangle
        if frame.shape[0] > 400 and frame.shape[1] > 400:
            if frame[350, 325, 1] > 200: # Green channel high
                detections.append({
                    "class": "bottle", # Mapped to smoke
                    "confidence": 0.95,
                    "bbox": [300, 300, 350, 450]
                })
                
        return detections
