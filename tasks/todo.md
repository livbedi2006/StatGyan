# Task List: High-Accuracy ML Models, Overfitting Validation & SIH Prototype Polish

- [ ] Task 1: Create Grounded Competency Dataset (`data/datasets/competency_training_corpus.json`)
  - Acceptance: A high-quality, balanced 150+ statement corpus across all 6 official MoSPI domains.
  - Verify: File exists and contains at least 25 entries per domain with official terminology.
  - Files: `data/datasets/competency_training_corpus.json`

- [ ] Task 2: Build & Calibrate ML Models with Anti-Overfitting Guards (`ml_engine/competency_model.py`, `ml_engine/survey_ml_model.py`)
  - Acceptance: Train-test split (80/20) with L2 regularized model achieving >= 92% train acc, >= 90% test acc, and |train - test| <= 5%.
  - Verify: Model script executes train/test evaluation and prints accuracy and cross-validation metrics.
  - Files: `ml_engine/competency_model.py`, `ml_engine/survey_ml_model.py`

- [ ] Task 3: Simplify and Align Engine APIs across all 7 Models (`ml_engine/*.py`)
  - Acceptance: Clean polymorphic signatures, standard aliases (`CompetencyModel`, `MCQGenerator`, `BlendedRecommender`, `DecayModel`, `PredictiveAnalytics`), no duplicate code.
  - Verify: All engine modules can be imported and executed without errors.
  - Files: `ml_engine/competency_model.py`, `ml_engine/mcq_generator.py`, `ml_engine/recommender_model.py`, `ml_engine/decay_model.py`, `ml_engine/predictive_analytics.py`, `ml_engine/virtual_lab_evaluator.py`

- [ ] Task 4: Implement Comprehensive TDD Test Suites (`tests/test_ml_accuracy.py`, `tests/test_all_models.py`)
  - Acceptance: `test_ml_accuracy.py` tests and confirms train acc >= 92%, test acc >= 90%, generalization gap <= 5%, 5-fold CV >= 90%; `test_all_models.py` passes all 7 engine tests with 100% pass rate.
  - Verify: Run `python -m unittest tests/test_ml_accuracy.py` and `python -m unittest tests/test_all_models.py`.
  - Files: `tests/__init__.py`, `tests/test_ml_accuracy.py`, `tests/test_all_models.py`

- [ ] Task 5: Sync Root `index.html` & Verify End-to-End via Browser Subagent
  - Acceptance: Root `index.html` matches `static/index.html`; browser subagent navigates the 7-step Jury Demo Tour and inspects the SIH Solution Docket Modal with zero console errors.
  - Verify: Subagent returns complete report and records demo video artifact.
  - Files: `index.html`, `static/index.html`, `walkthrough.md`

- [ ] Task 6: Knowledge Graph Update (`graphify update .`)
  - Acceptance: Knowledge graph updated with all new modules and relations without errors.
  - Verify: Run `python -m graphify update .`.
