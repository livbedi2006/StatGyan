"""
StatGyan AI - Machine Learning Model Accuracy & Anti-Overfitting Test Suite
Strictly verifies that custom MoSPI models achieve high accuracy on datasets
and exhibit NO overfitting on held-out test data and cross-validation folds.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml_engine.competency_model import CompetencyGapModel
from ml_engine.survey_ml_model import SurveyMicrodataMLModel


class TestMLModelAccuracyAndGeneralization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.competency_model = CompetencyGapModel()
        cls.survey_model = SurveyMicrodataMLModel()

    def test_01_competency_model_high_accuracy(self):
        """
        Asserts Competency NLP Model achieves high accuracy on dataset.
        Requirement: train_accuracy >= 92%, test_accuracy >= 90%.
        """
        metrics = self.competency_model.evaluate_model_accuracy()
        
        self.assertGreaterEqual(
            metrics["train_accuracy"], 0.92,
            f"Train accuracy {metrics['train_accuracy']} below required 92% threshold"
        )
        self.assertGreaterEqual(
            metrics["test_accuracy"], 0.90,
            f"Test accuracy {metrics['test_accuracy']} below required 90% threshold"
        )
        self.assertGreaterEqual(
            metrics["cv_mean_accuracy"], 0.90,
            f"5-Fold CV accuracy {metrics['cv_mean_accuracy']} below required 90% threshold"
        )

    def test_02_competency_model_no_overfitting(self):
        """
        Explicitly verifies that the Competency Model does NOT overfit.
        Guarantees that generalization gap (|train_acc - test_acc|) is <= 5.0%.
        """
        metrics = self.competency_model.evaluate_model_accuracy()
        gap = metrics["generalization_gap"]
        
        self.assertLessEqual(
            gap, 0.05,
            f"Overfitting detected! Generalization gap {gap*100:.2f}% exceeds 5.0% threshold"
        )
        self.assertTrue(metrics["no_overfitting_verified"])
        self.assertEqual(metrics["status"], "VERIFIED_HIGH_ACCURACY_NO_OVERFITTING")

    def test_03_competency_model_unseen_task_generalization(self):
        """
        Evaluates the Competency Model on completely novel out-of-sample statements.
        Confirms robust domain inference on unscripted officer self-evaluations.
        """
        test_cases = [
            (
                "National Accounts & GDP Estimation",
                "Compiled state-level annual Gross Value Added by economic activity adhering to SNA 2008 standards."
            ),
            (
                "Index Numbers (CPI & IIP)",
                "Aggregated price relatives for monthly Consumer Price Index numbers applying modified Laspeyres with consumption weights."
            ),
            (
                "Data Analytics & Programming",
                "Wrote Python and pandas automated routines for microdata ingestion into our PostgreSQL repository."
            ),
            (
                "Field Operations & CAPI Validation",
                "Conducted household visits with CAPI device for schedule 10.4 and verified geo-tagging stamps."
            ),
            (
                "Official Statistics Governance & Quality",
                "Audited survey procedures against NQAF guidelines and ensured statistical disclosure control."
            )
        ]

        for expected_domain, statement in test_cases:
            inferred = self.competency_model.infer_competency_from_text(statement)
            top_domain = max(inferred.items(), key=lambda x: x[1])[0]
            self.assertEqual(
                top_domain, expected_domain,
                f"Failed generalization: expected '{expected_domain}', got '{top_domain}' for statement: '{statement}'"
            )
            # Ensure top domain has elevated proficiency score
            self.assertGreater(inferred[top_domain], 70.0)

    def test_04_survey_microdata_ml_model_anti_overfitting(self):
        """
        Tests the statistical survey demographic classifier for PLFS labour force prediction.
        Verifies test generalization gap <= 5.0% and stable 5-fold cross-validation.
        """
        metrics = self.survey_model.evaluate_model_accuracy()
        
        self.assertGreaterEqual(metrics["train_accuracy"], 0.70)
        self.assertGreaterEqual(metrics["test_accuracy"], 0.70)
        self.assertLessEqual(
            metrics["generalization_gap"], 0.05,
            f"Overfitting on survey demographic clusters! Gap: {metrics['generalization_gap']}"
        )
        self.assertTrue(metrics["no_overfitting_verified"])
        self.assertEqual(metrics["status"], "VERIFIED_NO_OVERFITTING")

    def test_05_survey_microdata_predictions(self):
        """
        Verifies individual predictions match MoSPI empirical demographic expectations.
        """
        # Prime age male in urban sector -> High probability of labour force participation
        prime_male = self.survey_model.predict_status(age=35, is_male=True, is_urban=True)
        self.assertTrue(prime_male["in_labour_force"])
        self.assertGreater(prime_male["labour_force_probability"], 0.70)

        # School age youth (16) -> Low probability of labour force participation (predominantly in education)
        youth = self.survey_model.predict_status(age=16, is_male=False, is_urban=False)
        self.assertLess(youth["labour_force_probability"], 0.50)


if __name__ == "__main__":
    unittest.main()
