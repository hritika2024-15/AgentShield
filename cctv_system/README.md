# Multi-Agent CCTV Surveillance AI System

A multi-agent AI system for real-time CCTV surveillance using **YOLO** object detection, **Gemini AI** reporting, and automated incident response.

## 🎯 Features

- **5 Specialized Agents** working in coordination
- **Real-time Anomaly Detection** (fire, smoke, weapons, falls, fights, accidents, theft)
- **3-Frame Confirmation Rule** to reduce false positives
- **Automated Emergency Response** simulation
- **AI-Powered Reports** via Gemini (with fallback)
- **Persistent Long-Term Memory** (incidents saved to JSON)
- **Structured Logging** (JSON format)

## 🏗️ Architecture

```
VideoFrameExtractor → FrameAnalyzer → ConfidenceAggregator → EmergencyResponder → ReportGenerator
     (VideoTool)       (YOLOTool)      (3-frame rule)       (EmergencyTool)    (GeminiTool)
```

### Agent Workflow

1. **VideoFrameExtractorAgent** - Extracts frames from video
2. **FrameAnalyzerAgent** - Detects anomalies using YOLO
3. **ConfidenceAggregatorAgent** - Applies 3-frame confirmation rule
4. **EmergencyResponderAgent** - Triggers simulated emergency actions
5. **ReportGeneratorAgent** - Generates AI-powered reports

### Memory System

- **Short-term Memory**: Rolling 3-frame window for incident confirmation
- **Long-term Memory**: All confirmed incidents persisted to `data/incident_history.json`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

Get your API key: https://aistudio.google.com/apikey

### 3. Run with Sample Video (Quick Demo)

The repository includes a sample test video. Just run:
```bash
python main.py
```

**Or** use your own video by editing `config.py`:
```python
VIDEO_SOURCE = "path/to/your/video.mp4"
```

## 📁 Project Structure

```
cctv_system/
├── agents/              # Specialized agents
│   ├── frame_extractor.py
│   ├── frame_analyzer.py
│   ├── aggregator.py
│   ├── responder.py
│   └── reporter.py
├── tools/               # Reusable tools
│   ├── video_tool.py
│   ├── yolo_tool.py
│   ├── emergency_tool.py
│   └── gemini_tool.py
├── utils/              
│   ├── logger.py        # JSON logging
│   └── memory.py        # Shared memory with persistence
├── data/               
│   ├── snapshots/       # Incident frame captures
│   ├── incident_history.json  # Long-term memory
│   └── final_report.md  # AI-generated reports
├── logs/                # System logs
├── main.py              # Main orchestrator
├── config.py            # Configuration
└── .env                 # API keys (not committed)
```

## ⚙️ Configuration

Edit `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `VIDEO_SOURCE` | `data/sample_video.mp4` | Video file  |
| `YOLO_MODEL_PATH` | `yolov8n.pt` | YOLO model weights |
| `CONFIDENCE_THRESHOLD` | `0.5` | Detection confidence threshold |
| `OUTPUT_DIR` | `data` | Output directory |

## 📊 Outputs

- **Logs**: `logs/system.log` (JSON format)
- **Snapshots**: `data/snapshots/frame_*.jpg`
- **Reports**: `data/final_report.md` (AI-generated)
- **Memory**: `data/incident_history.json` (persistent)

## 🧠 Memory & Persistence

### Short-Term Memory
- Last 3 frames in rolling window
- Used for 3-frame confirmation rule
- Cleared after session

### Long-Term Memory
- All confirmed incidents with full details
- **Automatically saved** to `data/incident_history.json`
- Persists between runs
- Includes: incident type, confidence, timestamp, location, snapshot path, actions taken


## 🔧 Tools (Agent-Tool Pattern)

Each tool encapsulates specific functionality:

- **VideoTool** - OpenCV video capture and streaming
- **YOLOTool** - YOLO object detection
- **EmergencyTool** - Emergency response simulation
- **GeminiTool** - AI report generation (with mock fallback)

## 🎓 Key Concepts

### 3-Frame Confirmation Rule
Reduces false positives by requiring the same anomaly to appear in 3 consecutive frames before confirming an incident.

### Agent-Tool Pattern
Agents delegate specialized work to tools, enabling:
- Loose coupling
- Easy testing and mocking
- Tool reusability across agents

### Singleton Memory
All agents share the same `SharedMemory` instance for coordination and state management.

## 🧪 Testing

Generate synthetic test video:
```bash
python utils/video_gen.py
```

This creates `data/sample_video.mp4` with a green rectangle for testing.

## 📝 Example Output

```
[MEMORY] No existing memory file found, starting fresh
[OK] Gemini API key found (length: 39)
[OK] Gemini model initialized: gemini-2.5-pro

2025-11-25 00:38:15 - ConfidenceAggregatorAgent - INFO - Potential theft detected (Count: 1)
2025-11-25 00:38:15 - ConfidenceAggregatorAgent - INFO - Potential theft detected (Count: 2)
2025-11-25 00:38:15 - ConfidenceAggregatorAgent - INFO - Potential theft detected (Count: 3)
2025-11-25 00:38:15 - ConfidenceAggregatorAgent - INFO - CONFIRMED INCIDENT: theft
2025-11-25 00:38:15 - EmergencyResponderAgent - INFO - INITIATING EMERGENCY RESPONSE FOR: theft

[MEMORY] Saved 1 incidents to data/incident_history.json
[AI] Generating AI-powered report with Gemini...
[OK] Gemini report generated successfully!
```

## 💻 Supported Video Formats

- `.mp4` (recommended)
- `.avi`
- `.mov`
- `.mkv`
- Live camera (set `VIDEO_SOURCE = 0`)

## 📚 Dependencies

- `opencv-python` - Video processing
- `ultralytics` - YOLO detection
- `google-generativeai` - Gemini AI
- `python-dotenv` - Environment variables
- `Pillow`, `numpy` - Image processing

## 🔍 Observability

- **Structured Logs**: JSON format in `logs/system.log`
- **Debug Messages**: `[OK]`, `[WARN]`, `[ERROR]`, `[AI]`, `[MOCK]`, `[MEMORY]`
- **Incident History**: Full audit trail in `incident_history.json`


## Acknowledgments

- **Ultralytics YOLO** - Object detection
- **Google Gemini** - AI report generation
- **OpenCV** - Video processing

---

**Multi-Agent AI System demonstrating agent coordination, tool usage, and persistent memory** 🤖
