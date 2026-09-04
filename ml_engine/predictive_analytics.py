"""
StatGyan AI - Cadre Readiness Forecaster & HR Heatmap Analytics
Aggregates capability profiles across MoSPI divisions and regional directorates.
Predicts statistical survey readiness and deployment shortfall risks.
"""

from typing import Dict, List, Any
import numpy as np

DIVISIONS = [
    {
        "id": "FOD",
        "name": "Field Operations Division (FOD)",
        "headquarters": "New Delhi / 6 Zonal & 49 Regional Offices",
        "cadre_strength": 6450,
        "primary_focus": "Primary data collection, CAPI execution, sample listing",
        "avg_scores": {
            "Survey Methodology & Sampling": 68.4,
            "National Accounts & GDP Estimation": 34.2,
            "Index Numbers (CPI & IIP)": 62.1,
            "Data Analytics & Programming": 42.5,
            "Field Operations & CAPI Validation": 91.2,
            "Official Statistics Governance & Quality": 61.0
        }
    },
    {
        "id": "SDRD",
        "name": "Survey Design and Research Division (SDRD)",
        "headquarters": "Kolkata, West Bengal",
        "cadre_strength": 420,
        "primary_focus": "Sampling designs, schedules preparation, tabulation plans",
        "avg_scores": {
            "Survey Methodology & Sampling": 93.5,
            "National Accounts & GDP Estimation": 64.0,
            "Index Numbers (CPI & IIP)": 78.2,
            "Data Analytics & Programming": 82.0,
            "Field Operations & CAPI Validation": 80.5,
            "Official Statistics Governance & Quality": 85.0
        }
    },
    {
        "id": "NAD",
        "name": "National Accounts Division (NAD)",
        "headquarters": "New Delhi",
        "cadre_strength": 310,
        "primary_focus": "Annual & quarterly GDP estimates, GVA, SUT, capital stock",
        "avg_scores": {
            "Survey Methodology & Sampling": 72.0,
            "National Accounts & GDP Estimation": 94.6,
            "Index Numbers (CPI & IIP)": 84.1,
            "Data Analytics & Programming": 79.5,
            "Field Operations & CAPI Validation": 55.0,
            "Official Statistics Governance & Quality": 91.0
        }
    },
    {
        "id": "ESD",
        "name": "Economic Statistics Division (ESD)",
        "headquarters": "New Delhi",
        "cadre_strength": 380,
        "primary_focus": "CPI Compilation, IIP Index, Business Registers, ASI",
        "avg_scores": {
            "Survey Methodology & Sampling": 75.2,
            "National Accounts & GDP Estimation": 78.5,
            "Index Numbers (CPI & IIP)": 94.8,
            "Data Analytics & Programming": 77.0,
            "Field Operations & CAPI Validation": 68.0,
            "Official Statistics Governance & Quality": 87.5
        }
    },
    {
        "id": "DIID",
        "name": "Data Informatics & Innovation Division (DIID)",
        "headquarters": "New Delhi / Computer Centre",
        "cadre_strength": 290,
        "primary_focus": "MoSPI MCP Server, data lake, AI/ML use cases, IT infrastructure",
        "avg_scores": {
            "Survey Methodology & Sampling": 71.0,
            "National Accounts & GDP Estimation": 58.0,
            "Index Numbers (CPI & IIP)": 70.0,
            "Data Analytics & Programming": 93.4,
            "Field Operations & CAPI Validation": 84.2,
            "Official Statistics Governance & Quality": 89.0
        }
    }
]

UPCOMING_SURVEY_PIPELINES = [
    {
        "survey_id": "SURVEY-81ST-NSS",
        "title": "81st Round National Socio-Economic Survey",
        "launch_date": "Q1 2027",
        "required_competency_focus": {
            "Survey Methodology & Sampling": 85.0,
            "Field Operations & CAPI Validation": 90.0
        },
        "critical_divisions": ["FOD", "SDRD"]
    },
    {
        "survey_id": "SURVEY-CPI-REVISION",
        "title": "National CPI Base Revision Rollout",
        "launch_date": "Q3 2026",
        "required_competency_focus": {
            "Index Numbers (CPI & IIP)": 90.0,
            "Data Analytics & Programming": 80.0
        },
        "critical_divisions": ["ESD", "DIID"]
    },
    {
        "survey_id": "SURVEY-ECONOMIC-CENSUS",
        "title": "All-India Economic Census & ASI Modernization",
        "launch_date": "Q4 2026",
        "required_competency_focus": {
            "Field Operations & CAPI Validation": 92.0,
            "Data Analytics & Programming": 75.0
        },
        "critical_divisions": ["FOD", "ESD", "DIID"]
    }
]

class PredictiveAnalyticsEngine:
    def __init__(self):
        self.divisions = DIVISIONS
        self.pipelines = UPCOMING_SURVEY_PIPELINES

    def get_divisional_heatmap(self) -> Dict[str, Any]:
        """
        Returns divisional capability matrix for admin heatmaps.
        """
        matrix = []
        for div in self.divisions:
            matrix.append({
                "division_id": div["id"],
                "division_name": div["name"],
                "strength": div["cadre_strength"],
                "competencies": div["avg_scores"]
            })
        return {
            "divisions_count": len(self.divisions),
            "total_cadre_strength": sum(d["cadre_strength"] for d in self.divisions),
            "heatmap_data": matrix
        }

    def forecast_survey_readiness(self) -> List[Dict[str, Any]]:
        """
        Simulates readiness & shortfall risk for upcoming official statistical surveys.
        """
        forecasts = []
        for survey in self.pipelines:
            critical_divs = [d for d in self.divisions if d["id"] in survey["critical_divisions"]]
            
            # Compute average score in required competencies across critical divisions
            req_focus = survey["required_competency_focus"]
            ratios = []
            for div in critical_divs:
                for comp, target in req_focus.items():
                    act = div["avg_scores"].get(comp, 50.0)
                    ratios.append(min(1.0, act / target))

            readiness_pct = round(float(np.mean(ratios)) * 100.0, 1)
            
            if readiness_pct >= 88.0:
                risk_level = "LOW RISK"
                status_color = "#10b981"  # green
                advice = "Cadre ready for field deployment. Routine refresher recommended."
            elif readiness_pct >= 75.0:
                risk_level = "MODERATE DEFICIT"
                status_color = "#f59e0b"  # amber
                advice = "Targeted iGOT digital modules required for regional FOD supervisors before deployment."
            else:
                risk_level = "HIGH RISK - CADRE GAP"
                status_color = "#ef4444"  # red
                advice = "Immediate mandatory NSSTA workshop required to prevent survey tabulation delays."

            forecasts.append({
                "survey_id": survey["survey_id"],
                "title": survey["title"],
                "launch_date": survey["launch_date"],
                "critical_divisions": survey["critical_divisions"],
                "readiness_pct": readiness_pct,
                "risk_level": risk_level,
                "status_color": status_color,
                "strategic_action": advice
            })

        return forecasts


# Backwards-compatible alias
PredictiveAnalytics = PredictiveAnalyticsEngine

