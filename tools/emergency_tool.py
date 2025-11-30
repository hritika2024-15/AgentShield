from config import EMERGENCY_TYPES

class EmergencyTool:
    def __init__(self):
        pass

    def trigger_response(self, incident_type):
        response_target = EMERGENCY_TYPES.get(incident_type, "General Emergency")
        
        actions = [
            f"Alert sent to {response_target}",
            f"Local alarm triggered for {incident_type}",
            "Building admin notified"
        ]
        
        return actions
