import os
import cv2
import time
from agents.frame_extractor import VideoFrameExtractorAgent
from agents.frame_analyzer import FrameAnalyzerAgent
from agents.aggregator import ConfidenceAggregatorAgent
from agents.responder import EmergencyResponderAgent
from agents.reporter import ReportGeneratorAgent
from utils.logger import setup_logger
from utils.memory import SharedMemory
from config import SNAPSHOT_DIR

def main():
    logger = setup_logger("MainSystem", "logs/system.log")
    logger.info("Starting Multi-Agent CCTV Surveillance System")

    # Initializing Agents
    extractor = VideoFrameExtractorAgent()
    analyzer = FrameAnalyzerAgent()
    aggregator = ConfidenceAggregatorAgent()
    responder = EmergencyResponderAgent()
    reporter = ReportGeneratorAgent()
    
    memory = SharedMemory()
    memory.reset_session()

    # Main Loop
    try:
        for frame_count, frame in extractor.run():
            if memory.session_state["incident_confirmed"]:
                logger.info("Incident confirmed. Stopping video processing.")
                break
            
            logger.info(f"Processing Frame {frame_count}")
            
            # 1. Analyze Frame
            detections = analyzer.run(frame)
            
            # Save snapshot for potential evidence
            snapshot_path = os.path.join(SNAPSHOT_DIR, f"frame_{frame_count}.jpg")
            cv2.imwrite(snapshot_path, frame)
            
            # 2. Aggregate & Check for Incidents
            confirmed_incidents = aggregator.run(detections, frame_count, snapshot_path)
            
            # 3. Respond to Incidents
            for incident in confirmed_incidents:
                responder.run(incident)
                
                # 4. Generate Report
                report_path = reporter.run(incident)
                logger.info(f"System finished. Report available at: {report_path}")
                
                # Stop after one incident as per requirements
                return

            

    except KeyboardInterrupt:
        logger.info("System stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info("System shutdown.")

if __name__ == "__main__":
    main()
