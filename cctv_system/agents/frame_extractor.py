from agents.base_agent import BaseAgent
from tools.video_tool import VideoTool

class VideoFrameExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__("VideoFrameExtractorAgent")
        self.video_tool = VideoTool()
    
    def run(self):
        self.log(f"Starting video extraction from {self.video_tool.video_source}")
        
        try:
            for frame_count, frame in self.video_tool.stream_frames():
                yield frame_count, frame
        except Exception as e:
            self.log(f"Error during video extraction: {e}", "error")

        self.log("Video extraction finished")
