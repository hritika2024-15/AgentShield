from agents.base_agent import BaseAgent
from utils.memory import SharedMemory

class ConfidenceAggregatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ConfidenceAggregatorAgent")
        self.memory = SharedMemory()
        self.consecutive_detections = {} # {class_name: count}
        self.required_consecutive_frames = 3

    def run(self, detections, frame_count, snapshot_path):
        current_classes = set()
        
        # Check for relevant anomalies
        # Mapping standard YOLO classes to our target anomalies for DEMO purposes
        # In a real system, we would train a custom model.
        anomaly_mapping = {
            "person": "theft", # Simulating theft detection
            "car": "accident", # Simulating accident
            "fire hydrant": "fire", # Simulating fire
            "bottle": "smoke", # Simulating smoke
            "knife": "weapon",
            "scissors": "weapon"
        }

        detected_anomalies = []

        for det in detections:
            cls_name = det["class"]
            confidence = det["confidence"]
            
            # Map to target anomaly if applicable
            anomaly_type = anomaly_mapping.get(cls_name)
            
            if anomaly_type:
                current_classes.add(anomaly_type)
                
                # Update consecutive count
                self.consecutive_detections[anomaly_type] = self.consecutive_detections.get(anomaly_type, 0) + 1
                
                self.log(f"Potential {anomaly_type} detected (Count: {self.consecutive_detections[anomaly_type]})")

                if self.consecutive_detections[anomaly_type] >= self.required_consecutive_frames:
                    # Confirm incident
                    if not self.memory.session_state["incident_confirmed"]:
                        self.log(f"CONFIRMED INCIDENT: {anomaly_type}")
                        incident_record = self.memory.confirm_incident(anomaly_type, confidence, snapshot_path)
                        detected_anomalies.append(incident_record)
            
        # Reset counts for classes not found in this frame
        for cls in list(self.consecutive_detections.keys()):
            if cls not in current_classes:
                self.consecutive_detections[cls] = 0
        
        return detected_anomalies
