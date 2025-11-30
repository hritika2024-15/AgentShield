import cv2
import numpy as np
import os

def create_test_video(filename="data/sample_video.mp4", duration=5, fps=5):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    height, width = 640, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    frames = duration * fps
    
    for i in range(frames):
        # Create a black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add some text/shapes
        cv2.putText(frame, f"Frame {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Simulate a "person" (which we mapped to theft) appearing after frame 10
        if i > 10:
            # Draw a stick figure or just a rectangle that looks like a person to a human, 
            # but for YOLO we need something realistic or we just hope it detects *something*.
            # Actually, drawing a simple shape won't trigger YOLO trained on real images easily.
            # We might need to rely on the fact that we are using a real model.
            # If we can't generate a realistic video, we might fail detection.
            # However, for the purpose of this task, I will try to paste a real image of a person if I had one.
            # Since I don't, I will rely on the user providing a video OR I will try to create a very simple "person" blob
            # and hope for the best, OR I will mock the detection in the analyzer for testing purposes if the model fails.
            # BUT, I should try to make it work.
            # Let's draw a white rectangle. YOLO might detect it as a 'tv' or 'laptop' or something.
            # We mapped 'person', 'car', 'fire hydrant', 'bottle'.
            # A red circle might look like a ball (sports ball).
            # A bottle shape?
            
            # Let's draw a "bottle" (simple rectangle with a neck)
            cv2.rectangle(frame, (300, 300), (350, 450), (0, 255, 0), -1) # Green bottle body
            cv2.rectangle(frame, (315, 280), (335, 300), (0, 255, 0), -1) # Neck
            
            # We mapped 'bottle' -> 'smoke'.
            pass
            
        out.write(frame)
    
    out.release()
    print(f"Test video created at {filename}")

if __name__ == "__main__":
    create_test_video()
