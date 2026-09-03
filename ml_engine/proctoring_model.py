"""
StatGyan AI - AI Proctoring & Restriction Engine
Integrates anti-cheating restrictions, extension blocking heuristics,
face/gaze anomaly detection, and real-time candidate trust scoring.
"""

from typing import Dict, List, Any, Optional
import time

# Known unauthorized AI tools & extension signatures
RESTRICTED_AI_EXTENSIONS = [
    {"name": "ChatGPT / OpenAI Sidebar", "signature": "chatgpt-sidebar, #__next_chatgpt"},
    {"name": "Monica AI Copilot", "signature": "monica-root, [data-monica]"},
    {"name": "Merlin AI Assistant", "signature": "#merlin-popup, .merlin-companion"},
    {"name": "Sider AI Sidebar", "signature": "sider-root, [data-sider]"},
    {"name": "QuillBot Paraphraser", "signature": ".quillbot-extension"},
    {"name": "MaxAI Copilot", "signature": "#maxai-root"},
    {"name": "SciSpace / PaperGPT", "signature": ".scispace-highlighter"}
]

class ProctoringTrustEngine:
    def __init__(self):
        self.active_sessions = {}

    def start_session(self, session_id: str, candidate_name: str, cadre_id: str) -> Dict[str, Any]:
        session = {
            "session_id": session_id,
            "candidate_name": candidate_name,
            "cadre_id": cadre_id,
            "start_time": time.time(),
            "trust_score": 100,
            "strike_count": 0,
            "max_strikes": 3,
            "status": "SECURE_LOCKED",
            "incidents": []
        }
        self.active_sessions[session_id] = session
        return session

    def log_incident(
        self,
        session_id: str,
        incident_type: str,
        details: str,
        severity: str = "MEDIUM"
    ) -> Dict[str, Any]:
        session = self.active_sessions.get(session_id)
        if not session:
            session = self.start_session(session_id, "Official Candidate", "jso")

        penalty = 0
        if severity == "HIGH":
            penalty = 25
            session["strike_count"] += 1
        elif severity == "MEDIUM":
            penalty = 12
        else:
            penalty = 5

        session["trust_score"] = max(0, session["trust_score"] - penalty)
        
        # Check if exam should be locked
        if session["strike_count"] >= session["max_strikes"] or session["trust_score"] <= 35:
            session["status"] = "AUTOMATIC_FREEZE"

        incident_record = {
            "timestamp": time.strftime("%H:%M:%S"),
            "type": incident_type,
            "severity": severity,
            "penalty_applied": penalty,
            "details": details,
            "remaining_trust": session["trust_score"],
            "current_strikes": session["strike_count"]
        }
        session["incidents"].append(incident_record)

        return {
            "session_id": session_id,
            "status": session["status"],
            "trust_score": session["trust_score"],
            "strike_count": session["strike_count"],
            "max_strikes": session["max_strikes"],
            "is_frozen": session["status"] == "AUTOMATIC_FREEZE",
            "logged_incident": incident_record,
            "total_incidents": len(session["incidents"])
        }

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        duration = round((time.time() - session["start_time"]) / 60.0, 1)
        
        integrity_rating = "HIGH INTEGRITY"
        if session["trust_score"] < 50 or session["strike_count"] >= 3:
            integrity_rating = "INVALIDATED - INTEGRITY BREACH"
        elif session["trust_score"] < 75:
            integrity_rating = "FLAGGED FOR CADRE BOARD REVIEW"

        return {
            "session_id": session_id,
            "candidate_name": session["candidate_name"],
            "cadre": session["cadre_id"],
            "duration_minutes": duration,
            "final_trust_score": session["trust_score"],
            "strikes_accumulated": session["strike_count"],
            "integrity_rating": integrity_rating,
            "status": session["status"],
            "audit_trail": session["incidents"]
        }

    def get_security_policy(self) -> Dict[str, Any]:
        return {
            "browser_lockdown_rules": [
                "Fullscreen lockdown mode enforced",
                "DevTools / Inspect element (F12, Ctrl+Shift+I) blocked",
                "Context menu (Right-click) disabled",
                "Clipboard copy/paste blocked",
                "Tab-switching & window blur detection",
                "Browser extension DOM-injection scanner enabled",
                "Virtual machine / second monitor detection"
            ],
            "restricted_extensions": RESTRICTED_AI_EXTENSIONS
        }
