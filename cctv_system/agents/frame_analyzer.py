from agents.base_agent import BaseAgent
from tools.yolo_tool import YOLOTool

class FrameAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("FrameAnalyzerAgent")
        self.yolo_tool = YOLOTool()

    def run(self, frame):
        # self.log("Analyzing frame...")
        return self.yolo_tool.detect(frame)
