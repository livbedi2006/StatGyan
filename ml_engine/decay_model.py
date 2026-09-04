"""
StatGyan AI - Skill Decay & Methodology Drift Predictor
Models skill retention decay over time using exponential loss: S(t) = S_0 * exp(-lambda * t)
Detects methodology drift when official survey guidelines or base years are revised.
Triggers proactive refresher alerts for cadre deployment readiness.
"""

import math
from typing import Dict, List, Any, Optional

# Domain decay constants (higher = faster depreciation if not reinforced)
DOMAIN_LAMBDAS = {
    "Data Analytics & Programming": 0.045,          # Software syntax & packages evolve fast
    "Index Numbers (CPI & IIP)": 0.030,             # Base revisions & imputation standards
    "National Accounts & GDP Estimation": 0.025,    # Annual methodological updates
    "Survey Methodology & Sampling": 0.020,         # Multi-stage design changes per round
    "Field Operations & CAPI Validation": 0.035,    # Tablet/Android app versions update regularly
    "Official Statistics Governance & Quality": 0.015
}

# Real-world MoSPI official revision triggers
METHODOLOGY_DRIFT_EVENTS = [
    {
        "event_id": "DRIFT-2026-CPI-BASE",
        "title": "National CPI Base Year Revision Notice (Base Shift)",
        "affected_domain": "Index Numbers (CPI & IIP)",
        "decay_shock_pct": 38.0,
        "urgency": "HIGH",
        "summary": "ESD announces transition to updated CPI base year with revised CES consumption weights and new item basket.",
        "action_required": "Mandatory 3-hour micro-refresher on updated Laspeyres chaining before next index compilation cycle."
    },
    {
        "event_id": "DRIFT-2026-PLFS-PANEL",
        "title": "NSS 80th Round Sampling Strategy Protocol Revision",
        "affected_domain": "Survey Methodology & Sampling",
        "decay_shock_pct": 32.0,
        "urgency": "MEDIUM",
        "summary": "SDRD introduces updated urban rotational panel replacement rules and revised sub-sample multiplier formulations.",
        "action_required": "Complete iGOT refresher module on rotational panel sampling weights."
    },
    {
        "event_id": "DRIFT-2026-CAPI-CRYPTO",
        "title": "CAPI Field App Upgrade: CSPro Cryptographic Hashing Protocol",
        "affected_domain": "Field Operations & CAPI Validation",
        "decay_shock_pct": 25.0,
        "urgency": "MEDIUM",
        "summary": "DIID mandates device-level biometric & GPS bounding verification prior to survey sync.",
        "action_required": "Self-paced simulation on offline CAPI conflict resolution."
    }
]

class SkillDecayModel:
    def __init__(self):
        self.drift_events = METHODOLOGY_DRIFT_EVENTS

    def compute_decay(
        self,
        base_competencies: Dict[str, float],
        months_since_last_trained: float = 8.0,
        active_events: List[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates decayed competency levels and flags critical drift alerts.
        """
        if active_events is None:
            active_events = ["DRIFT-2026-CPI-BASE"]  # Default active simulated event

        decayed_scores = {}
        decay_deltas = {}
        alerts = []

        # Find active drift events
        shock_by_domain = {}
        for ev in self.drift_events:
            if ev["event_id"] in active_events:
                shock_by_domain[ev["affected_domain"]] = ev
                alerts.append({
                    "event_id": ev["event_id"],
                    "title": ev["title"],
                    "domain": ev["affected_domain"],
                    "shock_impact": f"-{ev['decay_shock_pct']}% proficiency depreciation",
                    "urgency": ev["urgency"],
                    "summary": ev["summary"],
                    "action_required": ev["action_required"]
                })

        for domain, s0 in base_competencies.items():
            lam = DOMAIN_LAMBDAS.get(domain, 0.025)
            # S(t) = S0 * exp(-lambda * t)
            time_retained = s0 * math.exp(-lam * months_since_last_trained)

            # Apply methodology shock if applicable
            if domain in shock_by_domain:
                shock_pct = shock_by_domain[domain]["decay_shock_pct"]
                time_retained = time_retained * (1.0 - (shock_pct / 100.0))

            final_score = round(max(15.0, min(100.0, time_retained)), 1)
            delta = round(s0 - final_score, 1)

            decayed_scores[domain] = final_score
            decay_deltas[domain] = delta

        return {
            "months_simulated": months_since_last_trained,
            "decayed_competencies": decayed_scores,
            "competency_losses": decay_deltas,
            "active_drift_alerts": alerts
        }

    def simulate_decay(
        self,
        cadre_id: str = "jso",
        elapsed_months: float = 8.0,
        active_events: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Simulates skill decay for a specific cadre, returning decay_curve and drift alerts.
        """
        from ml_engine.competency_model import CompetencyGapModel
        gap_model = CompetencyGapModel()
        gap_res = gap_model.evaluate_gap(cadre_id)
        
        assessed = gap_res["radar_data"]["assessed"]
        labels = gap_res["radar_data"]["labels"]
        base_dict = {labels[i]: assessed[i] for i in range(len(labels))}

        res = self.compute_decay(
            base_competencies=base_dict,
            months_since_last_trained=elapsed_months,
            active_events=active_events
        )

        decay_curve = []
        for domain, s0 in base_dict.items():
            post_score = res["decayed_competencies"].get(domain, s0)
            decay_curve.append({
                "domain": domain,
                "baseline_score": s0,
                "post_decay_score": post_score,
                "loss": res["competency_losses"].get(domain, 0.0)
            })

        res["decay_curve"] = decay_curve
        return res


# Backwards-compatible alias
DecayModel = SkillDecayModel

