"""
StatGyan AI - Blended Learning Pathway Recommender
Bridges digital self-paced iGOT Karmayogi courses with physical NSSTA TPAC academy labs.
Generates an optimized, prerequisite-aware blended progression plan tailored to the officer's specific skill gaps.
"""

import json
from typing import Dict, List, Any

class BlendedPathwayRecommender:
    def __init__(self, courses_path: str = "data/courses.json"):
        with open(courses_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.igot_courses = data["igot_courses"]
            self.nssta_workshops = data["nssta_workshops"]

        self.igot_by_competency = {}
        for c in self.igot_courses:
            comp = c["competency"]
            self.igot_by_competency.setdefault(comp, []).append(c)

        self.nssta_by_competency = {}
        for w in self.nssta_workshops:
            comp = w["competency"]
            self.nssta_by_competency.setdefault(comp, []).append(w)

    def generate_pathway(self, competency_gap_result: Any = "jso") -> Dict[str, Any]:
        """
        Builds a sequenced blended pathway based on identified competency gaps.
        Accepts either a competency gap result dictionary or a cadre ID string (e.g. 'jso').
        """
        if isinstance(competency_gap_result, str):
            from ml_engine.competency_model import CompetencyGapModel
            gap_model = CompetencyGapModel()
            competency_gap_result = gap_model.evaluate_gap(competency_gap_result)

        domain_breakdown = competency_gap_result.get("domain_breakdown", [])
        
        # Sort domains by gap descending (prioritize highest gaps)
        sorted_domains = sorted(domain_breakdown, key=lambda x: x["gap"], reverse=True)
        
        blended_pathway = []
        total_online_hours = 0
        total_residential_days = 0
        total_credits = 0.0

        step_counter = 1
        for d in sorted_domains:
            domain_name = d["domain"]
            gap = d["gap"]
            if gap <= 0:
                continue  # No training needed

            igot_list = self.igot_by_competency.get(domain_name, [])
            nssta_list = self.nssta_by_competency.get(domain_name, [])

            # Phase 1: Online Digital Foundation (iGOT Karmayogi)
            for igot in igot_list:
                blended_pathway.append({
                    "step_order": step_counter,
                    "phase": "Phase 1: Digital Foundation",
                    "channel": "iGOT Karmayogi",
                    "domain": domain_name,
                    "targeted_gap_points": gap,
                    "course_code": igot["code"],
                    "title": igot["title"],
                    "format": igot["format"],
                    "duration": f"{igot['duration_hours']} hours",
                    "credits": igot["credits"],
                    "status": "Ready for One-Click Enrollment"
                })
                total_online_hours += igot["duration_hours"]
                total_credits += igot["credits"]
                step_counter += 1

            # Phase 2: In-Person Hands-On Academy Lab (NSSTA TPAC)
            # Only recommend residential workshop if gap is Moderate or Critical (>= 10 pts)
            if gap >= 10.0:
                for nssta in nssta_list:
                    blended_pathway.append({
                        "step_order": step_counter,
                        "phase": "Phase 2: In-Person Applied Lab",
                        "channel": "NSSTA TPAC (Greater Noida)",
                        "domain": domain_name,
                        "targeted_gap_points": gap,
                        "course_code": nssta["code"],
                        "title": nssta["title"],
                        "format": nssta["format"],
                        "duration": f"{nssta['duration_days']} days (Residential)",
                        "dates": nssta["next_dates"],
                        "location": nssta["location"],
                        "tpac_approval_ref": nssta["tpac_approval_ref"],
                        "prerequisite_required": nssta["prerequisite_igot_course"],
                        "status": "Nominations Open"
                    })
                    total_residential_days += nssta["duration_days"]
                    step_counter += 1

        return {
            "officer_cadre": competency_gap_result.get("cadre_title", "Official Statistician"),
            "total_pathway_steps": len(blended_pathway),
            "total_online_hours": total_online_hours,
            "total_residential_days": total_residential_days,
            "total_karmayogi_credits": round(total_credits, 1),
            "learning_pathway": blended_pathway
        }


# Backwards-compatible alias
BlendedRecommender = BlendedPathwayRecommender

