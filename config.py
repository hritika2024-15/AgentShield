import os
from dotenv import load_dotenv

load_dotenv()

# System Configuration
VIDEO_SOURCE = "data/sample_video.mp4" # Path to video file 
YOLO_MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5
FRAME_RATE = 5 # Process 1 frame every X seconds or just fixed FPS processing
OUTPUT_DIR = "data"
SNAPSHOT_DIR = os.path.join(OUTPUT_DIR, "snapshots")
LOG_DIR = "logs"

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Emergency Configuration
EMERGENCY_TYPES = {
    "fire": "Fire Department",
    "smoke": "Fire Department",
    "weapon": "Police",
    "fall": "Medical Unit",
    "fight": "Police",
    "accident": "Ambulance",
    "theft": "Police"
}
