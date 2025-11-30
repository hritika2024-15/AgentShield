import json
import os
from collections import deque
from datetime import datetime

class SharedMemory:
    _instance = None
    MEMORY_FILE = "data/incident_history.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedMemory, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.short_term_memory = deque(maxlen=3) # Rolling window of last 3 frames
        self.long_term_memory = self._load_long_term_memory() # Load from file if exists
        self.session_state = {
            "camera_id": "CAM-001",
            "location": "Main Entrance",
            "frame_count": 0,
            "incident_confirmed": False,
            "current_incident": None
        }
    
    def _load_long_term_memory(self):
        """Load long-term memory from file if it exists."""
        if os.path.exists(self.MEMORY_FILE):
            try:
                with open(self.MEMORY_FILE, "r") as f:
                    data = json.load(f)
                    print(f"[MEMORY] Loaded {len(data)} past incidents from {self.MEMORY_FILE}")
                    return data
            except Exception as e:
                print(f"[MEMORY] Error loading memory file: {e}")
                return []
        else:
            print(f"[MEMORY] No existing memory file found, starting fresh")
            return []
    
    def _save_long_term_memory(self):
        """Save long-term memory to file."""
        try:
            os.makedirs(os.path.dirname(self.MEMORY_FILE), exist_ok=True)
            with open(self.MEMORY_FILE, "w") as f:
                json.dump(self.long_term_memory, f, indent=2)
            print(f"[MEMORY] Saved {len(self.long_term_memory)} incidents to {self.MEMORY_FILE}")
        except Exception as e:
            print(f"[MEMORY] Error saving memory file: {e}")
    
    def add_frame_data(self, frame_data):
        """
        frame_data: {
            "timestamp": ...,
            "detections": [...],
            "snapshot_path": ...
        }
        """
        self.short_term_memory.append(frame_data)
    
    def get_recent_frames(self):
        return list(self.short_term_memory)

    def confirm_incident(self, incident_type, confidence, snapshot_path):
        self.session_state["incident_confirmed"] = True
        incident_record = {
            "id": len(self.long_term_memory) + 1,
            "type": incident_type,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "camera_id": self.session_state["camera_id"],
            "location": self.session_state["location"],
            "snapshot_path": snapshot_path,
            "actions": []
        }
        self.session_state["current_incident"] = incident_record
        self.long_term_memory.append(incident_record)
        
        # Auto-save to file after each incident
        self._save_long_term_memory()
        
        return incident_record

    def log_action(self, action):
        if self.session_state["current_incident"]:
            self.session_state["current_incident"]["actions"].append({
                "action": action,
                "timestamp": datetime.now().isoformat()
            })
            # Update the incident in long-term memory
            for incident in self.long_term_memory:
                if incident["id"] == self.session_state["current_incident"]["id"]:
                    incident["actions"] = self.session_state["current_incident"]["actions"]
            # Save after action is logged
            self._save_long_term_memory()

    def reset_session(self):
        self.session_state["frame_count"] = 0
        self.session_state["incident_confirmed"] = False
        self.session_state["current_incident"] = None
        self.short_term_memory.clear()
    
    def get_all_incidents(self):
        """Get all incidents from long-term memory."""
        return self.long_term_memory
    
    def get_incident_by_id(self, incident_id):
        """Get a specific incident by ID."""
        for incident in self.long_term_memory:
            if incident["id"] == incident_id:
                return incident
        return None
    
    def get_incidents_by_type(self, incident_type):
        """Get all incidents of a specific type."""
        return [inc for inc in self.long_term_memory if inc["type"] == incident_type]
