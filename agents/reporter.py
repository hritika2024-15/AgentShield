from agents.base_agent import BaseAgent
from tools.gemini_tool import GeminiTool

class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportGeneratorAgent")
        self.gemini_tool = GeminiTool()

    def run(self, incident_data):
        self.log("Generating final report...")
        
        report_path = self.gemini_tool.generate_report(incident_data)
            
        self.log(f"Report saved to {report_path}")
        return report_path
