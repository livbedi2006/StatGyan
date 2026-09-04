# Task List: High-Accuracy ML Models, Overfitting Validation & SIH Prototype Polish

- [x] Task 1: Create Grounded Competency Dataset (`data/datasets/competency_training_corpus.json`)
  - Acceptance: A high-quality, balanced 360-statement corpus across all 6 official MoSPI domains.
  - Verify: File exists and contains 60 entries per domain with official terminology.
  - Files: `data/datasets/competency_training_corpus.json`

- [x] Task 2: Build & Calibrate ML Models with Anti-Overfitting Guards (`ml_engine/competency_model.py`, `ml_engine/survey_ml_model.py`)
  - Acceptance: Train-test split (80/20) with L2 regularized model achieving >= 92% train acc, >= 90% test acc, and |train - test| <= 5%.
  - Verify: Model script executes train/test evaluation and prints accuracy and cross-validation metrics.
  - Files: `ml_engine/competency_model.py`, `ml_engine/survey_ml_model.py`

- [x] Task 3: Simplify and Align Engine APIs across all 7 Models (`ml_engine/*.py`)
  - Acceptance: Clean polymorphic signatures, standard aliases (`CompetencyModel`, `MCQGenerator`, `BlendedRecommender`, `DecayModel`, `PredictiveAnalytics`), no duplicate code.
  - Verify: All engine modules can be imported and executed without errors.
  - Files: `ml_engine/competency_model.py`, `ml_engine/mcq_generator.py`, `ml_engine/recommender_model.py`, `ml_engine/decay_model.py`, `ml_engine/predictive_analytics.py`, `ml_engine/virtual_lab_evaluator.py`

- [x] Task 4: Implement Comprehensive TDD Test Suites (`tests/test_ml_accuracy.py`, `tests/test_all_models.py`)
  - Acceptance: `test_ml_accuracy.py` tests and confirms train acc >= 92%, test acc >= 90%, generalization gap <= 5%, 5-fold CV >= 90%; `test_all_models.py` passes all 7 engine tests with 100% pass rate.
  - Verify: Run `python -m unittest tests/test_ml_accuracy.py` and `python -m unittest tests/test_all_models.py`. (12/12 tests passing).
  - Files: `tests/__init__.py`, `tests/test_ml_accuracy.py`, `tests/test_all_models.py`

- [x] Task 5: Fast API Architecture & Real-Time Model Introspection (`backend/server.py`, `static/js/app.js`, `static/index.html`)
  - Acceptance: Sub-5ms warm model inferences, pre-warmed lifespan loading, GZip compression, `/api/ml/metrics` live introspection, and UI connection badge.
  - Verify: HTTP benchmark confirms 2-5ms model latencies; UI status badge displays pre-warmed models.
  - Files: `backend/server.py`, `static/js/app.js`, `static/index.html`, `index.html`

- [x] Task 6: Knowledge Graph Update (`graphify update .`)
  - Acceptance: Knowledge graph updated with all new modules and relations without errors (834 nodes, 945 edges, 46 communities).
  - Verify: Run `python -m graphify update .`.
