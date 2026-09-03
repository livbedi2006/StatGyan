"""
StatGyan AI - Core FastAPI Server
Integrates all Machine Learning and Deep Learning models for the MoSPI / DIID
Competency-Based Learning & Assessment Platform (SIH ID 26101).
"""

import os
import json
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
from pydantic import BaseModel

from ml_engine.competency_model import CompetencyGapModel
from ml_engine.mcq_generator import GroundedMCQGenerator
from ml_engine.recommender_model import BlendedPathwayRecommender
from ml_engine.decay_model import SkillDecayModel
from ml_engine.predictive_analytics import PredictiveAnalyticsEngine
from ml_engine.virtual_lab_evaluator import VirtualLabEvaluator
from ml_engine.proctoring_model import ProctoringTrustEngine

app = FastAPI(
    title="StatGyan AI - MoSPI Competency Platform",
    description="Official AI/ML Competency & Assessment Engine for Ministry of Statistics and Programme Implementation (MoSPI) / DIID",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML Models
competency_engine = CompetencyGapModel()
mcq_engine = GroundedMCQGenerator()
pathway_engine = BlendedPathwayRecommender()
decay_engine = SkillDecayModel()
analytics_engine = PredictiveAnalyticsEngine()
lab_evaluator = VirtualLabEvaluator()
proctoring_engine = ProctoringTrustEngine()

# Request Models
class AnalyzeRequest(BaseModel):
    cadre_id: str = "jso"
    assessed_scores: Optional[Dict[str, float]] = None

class InferRequest(BaseModel):
    cadre_id: str = "jso"
    self_statement: str

class GenerateMCQRequest(BaseModel):
    manual_id: Optional[str] = None
    domain: Optional[str] = None
    bloom_level: Optional[str] = None
    count: int = 4

class DecaySimulateRequest(BaseModel):
    cadre_id: str = "jso"
    months: float = 8.0
    active_events: Optional[List[str]] = None

class LabEvaluateRequest(BaseModel):
    script_code: str

class ProctoringStartRequest(BaseModel):
    session_id: str = "SESSION-EXAM-001"
    candidate_name: str = "Rajesh Kumar Sharma"
    cadre_id: str = "jso"

class ProctoringEventRequest(BaseModel):
    session_id: str = "SESSION-EXAM-001"
    incident_type: str = "TAB_SWITCH"
    details: str = "Candidate switched window or lost browser focus"
    severity: str = "HIGH"

# ----------------- API Endpoints -----------------

@app.get("/api/health")
def health_check():
    return {
        "status": "ONLINE",
        "system": "StatGyan AI - MoSPI Official Platform",
        "models_loaded": [
            "CompetencyGapModel (TF-IDF & LSA)",
            "GroundedMCQGenerator (Bloom's Taxonomy + 3-Stage QC)",
            "BlendedPathwayRecommender (iGOT + NSSTA TPAC)",
            "SkillDecayModel (Exponential loss + Methodology Shock)",
            "PredictiveAnalyticsEngine (Divisional Heatmaps & Survey Forecaster)",
            "VirtualLabEvaluator (Complex Multiplier Microdata Grader)",
            "ProctoringTrustEngine (Extension Blocker & Anti-Cheat AI)"
        ]
    }

@app.get("/api/cadres")
def get_cadres():
    return {"cadres": competency_engine.cadres_data}

@app.post("/api/competency/analyze")
def analyze_competency(req: AnalyzeRequest):
    result = competency_engine.evaluate_gap(req.cadre_id, req.assessed_scores)
    return result

@app.post("/api/competency/infer")
def infer_competency(req: InferRequest):
    inferred_scores = competency_engine.infer_competency_from_text(req.self_statement)
    result = competency_engine.evaluate_gap(req.cadre_id, inferred_scores)
    result["inferred_raw"] = inferred_scores
    return result

@app.post("/api/assessment/generate")
def generate_assessment(req: GenerateMCQRequest):
    return mcq_engine.generate_assessment(
        manual_id=req.manual_id,
        domain=req.domain,
        bloom_level=req.bloom_level,
        count=req.count
    )

@app.get("/api/assessment/export/qti")
def export_qti(count: int = 4):
    assessment = mcq_engine.generate_assessment(count=count)
    xml_str = mcq_engine.export_qti(assessment)
    return PlainTextResponse(content=xml_str, media_type="application/xml")

@app.get("/api/assessment/export/moodle")
def export_moodle(count: int = 4):
    assessment = mcq_engine.generate_assessment(count=count)
    xml_str = mcq_engine.export_moodle_xml(assessment)
    return PlainTextResponse(content=xml_str, media_type="application/xml")

@app.post("/api/recommender/pathway")
def recommend_pathway(req: AnalyzeRequest):
    gap_result = competency_engine.evaluate_gap(req.cadre_id, req.assessed_scores)
    return pathway_engine.generate_pathway(gap_result)

@app.post("/api/decay/simulate")
def simulate_decay(req: DecaySimulateRequest):
    gap_result = competency_engine.evaluate_gap(req.cadre_id)
    assessed = gap_result["radar_data"]["assessed"]
    base_dict = {
        gap_result["radar_data"]["labels"][i]: assessed[i]
        for i in range(len(gap_result["radar_data"]["labels"]))
    }
    decay_result = decay_engine.compute_decay(
        base_competencies=base_dict,
        months_since_last_trained=req.months,
        active_events=req.active_events
    )
    return decay_result

@app.get("/api/cadre/analytics")
def cadre_analytics():
    heatmap = analytics_engine.get_divisional_heatmap()
    forecasts = analytics_engine.forecast_survey_readiness()
    return {
        "heatmap": heatmap,
        "readiness_forecasts": forecasts
    }

@app.post("/api/lab/evaluate")
def evaluate_lab_code(req: LabEvaluateRequest):
    return lab_evaluator.evaluate_submission(req.script_code)

@app.get("/api/proctoring/policy")
def get_proctoring_policy():
    return proctoring_engine.get_security_policy()

@app.post("/api/proctoring/start")
def start_proctoring_session(req: ProctoringStartRequest):
    return proctoring_engine.start_session(req.session_id, req.candidate_name, req.cadre_id)

@app.post("/api/proctoring/log_event")
def log_proctoring_event(req: ProctoringEventRequest):
    return proctoring_engine.log_incident(
        session_id=req.session_id,
        incident_type=req.incident_type,
        details=req.details,
        severity=req.severity
    )

@app.get("/api/proctoring/report")
def get_proctoring_report(session_id: str = "SESSION-EXAM-001"):
    return proctoring_engine.get_session_summary(session_id)

@app.get("/api/graph")
def get_knowledge_graph():
    """
    Returns nodes and edges connecting Cadres, Competencies, Manuals, and Courses.
    """
    nodes = []
    edges = []

    # Cadre nodes
    for c in competency_engine.cadres_data:
        nodes.append({"id": f"cadre_{c['id']}", "label": c["title"], "type": "Cadre", "color": "#1e3a8a"})

    # Domain / Competency nodes
    domains = [
        "Survey Methodology & Sampling",
        "National Accounts & GDP Estimation",
        "Index Numbers (CPI & IIP)",
        "Data Analytics & Programming",
        "Field Operations & CAPI Validation",
        "Official Statistics Governance & Quality"
    ]
    for d in domains:
        nodes.append({"id": f"dom_{d}", "label": d, "type": "Competency", "color": "#0284c7"})

    # Manual nodes
    for m in mcq_engine.corpus_data:
        nodes.append({"id": f"man_{m['id']}", "label": m["title"], "type": "Manual", "color": "#059669"})

    # Course nodes (iGOT & NSSTA)
    for ig in pathway_engine.igot_courses:
        nodes.append({"id": f"igot_{ig['id']}", "label": ig["title"], "type": "iGOT Course", "color": "#d97706"})

    for ns in pathway_engine.nssta_workshops:
        nodes.append({"id": f"nssta_{ns['id']}", "label": ns["title"], "type": "NSSTA Workshop", "color": "#7c3aed"})

    # Edges: Cadre -> Competency
    for c in competency_engine.cadres_data:
        for dom, req in c["required_competencies"].items():
            if req >= 75:
                edges.append({"from": f"cadre_{c['id']}", "to": f"dom_{dom}", "label": f"Mandatory ({req}%)"})

    # Edges: Competency -> Manual
    for m in mcq_engine.corpus_data:
        for sec in m["sections"]:
            edges.append({"from": f"dom_{sec['domain']}", "to": f"man_{m['id']}", "label": "Governed by"})

    # Edges: Competency -> Courses
    for ig in pathway_engine.igot_courses:
        edges.append({"from": f"dom_{ig['competency']}", "to": f"igot_{ig['id']}", "label": "Digital Training"})

    for ns in pathway_engine.nssta_workshops:
        edges.append({"from": f"dom_{ns['competency']}", "to": f"nssta_{ns['id']}", "label": "Physical Lab"})

    return {"nodes": nodes, "edges": edges}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")
