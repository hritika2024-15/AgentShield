import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables directly
print(f"[DEBUG] Current working directory: {os.getcwd()}")
print(f"[DEBUG] Looking for .env file at: {os.path.join(os.getcwd(), '.env')}")
print(f"[DEBUG] .env file exists: {os.path.exists('.env')}")

dotenv_loaded = load_dotenv()
print(f"[DEBUG] load_dotenv() returned: {dotenv_loaded}")

# Get configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"[DEBUG] os.getenv('GEMINI_API_KEY') returned: {repr(GEMINI_API_KEY)}")
print(f"[DEBUG] Type: {type(GEMINI_API_KEY)}")
print(f"[DEBUG] Bool value: {bool(GEMINI_API_KEY)}")
if GEMINI_API_KEY:
    print(f"[DEBUG] Length: {len(GEMINI_API_KEY)}")
    print(f"[DEBUG] First 20 chars: {GEMINI_API_KEY[:20]}")

OUTPUT_DIR = "data"

class GeminiTool:
    def __init__(self, api_key=None):
        # Use provided key or load from environment
        self.api_key = api_key or GEMINI_API_KEY
        print(f"\n{'='*60}")
        print(f"GeminiTool Initialization")
        print(f"{'='*60}")
        if self.api_key:
            print(f"[OK] Gemini API key found (length: {len(self.api_key)})")
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-pro')
                print(f"[OK] Gemini model initialized: gemini-2.5-pro")
            except Exception as e:
                print(f"[ERROR] Error initializing Gemini: {e}")
                self.model = None
        else:
            print(f"[WARN] No Gemini API key found - using mock report generator")
            print(f"  To enable Gemini reports:")
            print(f"  1. Get API key from: https://aistudio.google.com/apikey")
            print(f"  2. Add to .env file: GEMINI_API_KEY=your_key_here")
            self.model = None
        print(f"{'='*60}\n")

    def generate_report(self, incident_data):
        report_path = os.path.join(OUTPUT_DIR, "final_report.md")
        
        if self.model:
            try:
                print("\n[AI] Generating AI-powered report with Gemini...")
                prompt = f"""
                Generate a detailed security incident report based on the following data:
                {incident_data}
                
                The report should include:
                1. Executive Summary
                2. Incident Details (Type, Time, Location, Camera ID)
                3. Confidence Analysis
                4. Emergency Actions Taken
                5. Recommendations
                
                Format as Markdown.
                """
                response = self.model.generate_content(prompt)
                report_content = response.text
                print("[OK] Gemini report generated successfully!")
            except Exception as e:
                print(f"[ERROR] Error generating report with Gemini: {e}")
                print("  Falling back to mock report...")
                report_content = self._mock_report(incident_data)
        else:
            print("\n[MOCK] Generating mock report (no Gemini API key)...")
            report_content = self._mock_report(incident_data)
            
        with open(report_path, "w") as f:
            f.write(report_content)
            
        return report_path

    def _mock_report(self, data):
        return f"""
# Security Incident Report

**Date:** {data['timestamp']}
**Incident Type:** {data['type']}
**Location:** {data['location']}
**Camera ID:** {data['camera_id']}

## Summary
A {data['type']} incident was detected with {data['confidence']:.2f} confidence.

## Actions Taken
{chr(10).join(['- ' + a['action'] for a in data['actions']])}

## Snapshot
![Snapshot]({data['snapshot_path']})
"""
