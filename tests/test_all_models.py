"""
StatGyan AI - Master SIH 26101 Model Verification Suite
Tests all 7 custom ML/AI engines for mathematical correctness,
grounding integrity, and standards compliance.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml_engine.competency_model import CompetencyModel
from ml_engine.mcq_generator import MCQGenerator
from ml_engine.recommender_model import BlendedRecommender
from ml_engine.decay_model import DecayModel
from ml_engine.predictive_analytics import PredictiveAnalytics
from ml_engine.virtual_lab_evaluator import VirtualLabEvaluator
from ml_engine.proctoring_model import ProctoringTrustEngine


class TestStatGyanAIModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.competency = CompetencyModel()
        cls.mcq = MCQGenerator()
        cls.recommender = BlendedRecommender()
        cls.decay = DecayModel()
        cls.analytics = PredictiveAnalytics()
        cls.lab = VirtualLabEvaluator()
        cls.proctoring = ProctoringTrustEngine()

    def test_01_competency_gap_engine(self):
        """Engine 1: Competency Model (TF-IDF & LSA Vector Gap Scoring)"""
        res = self.competency.analyze_gap("jso")
        self.assertIn("cadre_title", res)
        self.assertIn("overall_readiness_pct", res)
        self.assertGreaterEqual(res["overall_readiness_pct"], 0.0)
        self.assertLessEqual(res["overall_readiness_pct"], 100.0)
        self.assertEqual(len(res["radar_data"]["labels"]), 6)
        
        # Test NLP inference
        statement = "Conducted 45 field household scrutinies for PLFS using CAPI tablets, resolved CWS status discrepancies, and calculated basic sampling weights."
        inferred = self.competency.infer_from_text("jso", statement)
        self.assertIn("domain_breakdown", inferred)
        self.assertGreater(len(inferred["domain_breakdown"]), 0)

    def test_02_grounded_mcq_and_qc(self):
        """Engine 2: Grounded Bloom's MCQ Generator & 3-Stage QC"""
        res = self.mcq.generate_assessment(manual_id="plfs_manual_vol1", bloom_level=None, count=4)
        self.assertGreaterEqual(res["total_generated"], 1)
        self.assertGreaterEqual(res["qc_pass_rate_pct"], 90.0)
        for item in res["items"]:
            self.assertTrue(item["qc_audit"]["passed"])
            self.assertGreaterEqual(item["qc_audit"]["grounding_confidence"], 0.70)
            self.assertIn("citation", item)

        # Test QTI 2.1 and Moodle export
        qti_xml = self.mcq.export_qti_xml(res["items"])
        self.assertIn("<assessmentItem", qti_xml)
        self.assertIn("xmlns=\"http://www.imsglobal.org/xsd/imsqti_v2p1\"", qti_xml)

        moodle_xml = self.mcq.export_moodle_xml(res["items"])
        self.assertIn("<quiz>", moodle_xml)

    def test_03_proctoring_trust_engine(self):
        """Engine 3: AI Proctoring & Restriction Engine"""
        session_id = "TEST-SESSION-001"
        start = self.proctoring.start_session(session_id, "Official Candidate", "jso")
        self.assertEqual(start["trust_score"], 100)
        self.assertEqual(start["strike_count"], 0)

        # Log High Severity Incident (Tab Switch)
        log1 = self.proctoring.log_incident(session_id, "TAB_SWITCH_ATTEMPT", "Candidate switched windows.", "HIGH")
        self.assertEqual(log1["strike_count"], 1)
        self.assertEqual(log1["trust_score"], 75)
        self.assertFalse(log1["is_frozen"])

        # Log AI Extension Injection (High Severity)
        log2 = self.proctoring.log_incident(session_id, "AI_EXTENSION_INJECTION", "ChatGPT DOM elements intercepted.", "HIGH")
        self.assertEqual(log2["strike_count"], 2)
        self.assertEqual(log2["trust_score"], 50)

        # Log 3rd Strike -> Trigger Auto-Freeze
        log3 = self.proctoring.log_incident(session_id, "UNAUTHORIZED_MULTIPLE_FACES", "Second face detected.", "HIGH")
        self.assertEqual(log3["strike_count"], 3)
        self.assertTrue(log3["is_frozen"])
        self.assertEqual(log3["status"], "AUTOMATIC_FREEZE")

    def test_04_blended_pathway_recommender(self):
        """Engine 4: Blended Learning Pathway (iGOT + NSSTA)"""
        path = self.recommender.generate_pathway("jso")
        self.assertIn("learning_pathway", path)
        self.assertGreater(path["total_pathway_steps"], 0)
        self.assertGreater(path["total_online_hours"], 0)
        self.assertGreater(path["total_residential_days"], 0)
        self.assertGreater(path["total_karmayogi_credits"], 0.0)

        # Verify dual channel inclusion (digital iGOT and residential NSSTA)
        channels = [s["channel"] for s in path["learning_pathway"]]
        has_igot = any("iGOT" in ch for ch in channels)
        has_nssta = any("NSSTA" in ch for ch in channels)
        self.assertTrue(has_igot)
        self.assertTrue(has_nssta)

    def test_05_decay_and_drift_model(self):
        """Engine 5: Skill Decay & Methodology Shock Forecaster"""
        res = self.decay.simulate_decay("jso", elapsed_months=8)
        self.assertIn("decay_curve", res)
        self.assertIn("active_drift_alerts", res)
        self.assertGreaterEqual(len(res["active_drift_alerts"]), 1)
        # Check that post-decay score is less than baseline
        for d in res["decay_curve"]:
            self.assertLessEqual(d["post_decay_score"], d["baseline_score"])

    def test_06_predictive_divisional_analytics(self):
        """Engine 6: Divisional Capability Heatmaps & Survey Readiness"""
        heatmap = self.analytics.get_divisional_heatmap()
        self.assertIn("heatmap_data", heatmap)
        self.assertEqual(len(heatmap["heatmap_data"]), 5)  # FOD, SDRD, NAD, ESD, DIID

        forecasts = self.analytics.forecast_survey_readiness()
        self.assertGreaterEqual(len(forecasts), 3)
        for f in forecasts:
            self.assertIn("readiness_pct", f)
            self.assertIn("strategic_action", f)

    def test_07_virtual_statistical_lab(self):
        """Engine 7: Virtual Statistical Lab on Synthetic PLFS Microdata"""
        correct_script = """
def calculate_plfs_metrics(records):
    tot_pop = sum(r['multiplier'] for r in records)
    employed_pop = sum(r['multiplier'] for r in records if r['ups_code'] in [11, 31, 51])
    unemployed_pop = sum(r['multiplier'] for r in records if r['ups_code'] == 81)
    labour_force = employed_pop + unemployed_pop
    
    wpr = (employed_pop / tot_pop) * 100.0
    lfpr = (labour_force / tot_pop) * 100.0
    ur = (unemployed_pop / labour_force) * 100.0
    
    return {"WPR": round(wpr, 2), "LFPR": round(lfpr, 2), "UR": round(ur, 2)}
"""
        eval_res = self.lab.evaluate_code(correct_script)
        self.assertEqual(eval_res["status"], "PASSED")
        self.assertEqual(eval_res["passed_checks"], 5)
        self.assertEqual(eval_res["total_checks"], 5)
        self.assertEqual(eval_res["metrics"]["WPR"], 48.29)
        self.assertEqual(eval_res["metrics"]["LFPR"], 63.25)
        self.assertEqual(eval_res["metrics"]["UR"], 23.65)


if __name__ == "__main__":
    unittest.main()
