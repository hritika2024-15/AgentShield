from agents.base_agent import BaseAgent
from utils.memory import SharedMemory
from tools.emergency_tool import EmergencyTool

class EmergencyResponderAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmergencyResponderAgent")
        self.memory = SharedMemory()
        self.emergency_tool = EmergencyTool()

    def run(self, incident_record):
        incident_type = incident_record["type"]
        
        self.log(f"INITIATING EMERGENCY RESPONSE FOR: {incident_type}")
        
        actions = self.emergency_tool.trigger_response(incident_type)
        
        for action in actions:
            self.log(f"Action taken: {action}")
            self.memory.log_action(action)
            
        return actions
