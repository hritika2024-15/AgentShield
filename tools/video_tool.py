import cv2
import time
from config import VIDEO_SOURCE, FRAME_RATE

class VideoTool:
    def __init__(self, source=VIDEO_SOURCE, fps=FRAME_RATE):
        self.video_source = source
        self.frame_rate = fps
        self.cap = None

    def open_source(self):
        # Check if source is int (webcam) or string (file)
        source = int(self.video_source) if str(self.video_source).isdigit() else self.video_source
        self.cap = cv2.VideoCapture(source)
        return self.cap.isOpened()

    def read_frame(self):
        if self.cap and self.cap.isOpened():
            return self.cap.read()
        return False, None

    def release(self):
        if self.cap:
            self.cap.release()

    def stream_frames(self):
        if not self.open_source():
            raise ValueError(f"Error opening video source: {self.video_source}")

        frame_count = 0
        while self.cap.isOpened():
            ret, frame = self.read_frame()
            
            if not ret:
                break
            
            frame_count += 1
            yield frame_count, frame
            
            # Simulate real-time processing if needed
            # time.sleep(1.0 / self.frame_rate)
        
        self.release()
