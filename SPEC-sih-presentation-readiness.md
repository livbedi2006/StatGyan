# Spec: SIH 2026 Presentation & Model Readiness (Problem Statement ID 26101)

## Objective
Elevate the **StatGyan AI Platform** into a showcase-ready, competition-winning prototype for **Smart India Hackathon (SIH) Problem Statement ID 26101** (*"Develop an AI-enabled competency-based learning & assessment system for MoSPI / DIID"*).

The system must allow SIH judges, Ministry officials, and cadre review boards to:
1. Experience an interactive **Jury Guided Tour** covering all 7 AI/ML engines in 2 minutes.
2. Review the **Grounded Competency Model** with dynamic radar visualization and NLP job description parsing.
3. Test the **Grounded Bloom's Taxonomy Assessment Studio** with 100% citation verification and QTI 2.1 export.
4. Stress-test the **Secure AI Proctoring & Restriction Engine** with live simulated attacks (tab switch, extension injection, gaze shift, collaborator detection).
5. Inspect the **Blended Learning Pathway** integrating digital iGOT modules with physical NSSTA Greater Noida workshops.
6. Run the **Virtual Statistical Lab** computing official PLFS indicators (WPR, LFPR, UR) on synthetic microdata.
7. Explore the **5-Lane Knowledge Graph** highlighting end-to-end career pathways without overlapping clutter.
8. Access a comprehensive **SIH Pitch & Technical Architecture Modal** directly in the interface.

## Tech Stack
- **Backend**: Python 3.11, FastAPI, Uvicorn, Scikit-Learn (TF-IDF, TruncatedSVD), NumPy, RapidFuzz.
- **Frontend**: Vanilla CSS (Government-grade Design System inspired by MoSPI / MeitY guidelines), Chart.js (Radar Charts), HTML5 Canvas with High-DPI scaling.
- **Knowledge Representation**: Graphify knowledge ontology (738 nodes, 793 edges).
- **Standards Compliance**: QTI 2.1 XML (National LMS), Moodle XML, SNA 2008, PLFS NSS 80th Round, CPI Guidelines 2024.

## Commands
```bash
# Start FastAPI backend server
uvicorn backend.server:app --host 127.0.0.1 --port 8080 --reload

# Update and verify knowledge graph
python -m graphify update .

# Run automated unit test suite for all 7 ML models
python -m unittest tests/test_models.py

# Launch OmniRoute gateway (optional high-tier fallback)
omniroute start
```

## Project Structure
```
StatGyan AI/
├── backend/
│   └── server.py                     # FastAPI REST API (7 ML model endpoints)
├── ml_engine/
│   ├── competency_model.py           # TF-IDF & LSA gap analysis
│   ├── mcq_generator.py              # Grounded Bloom items + 3-stage QC
│   ├── proctoring_model.py           # AI Trust Engine + Extension Sandboxing
│   ├── recommender_model.py          # Blended pathway recommender
│   ├── decay_model.py                # Exponential skill decay & shock alerts
│   ├── predictive_analytics.py       # Divisional heatmaps & survey forecaster
│   └── virtual_lab_evaluator.py      # Synthetic PLFS microdata auto-grader
├── data/
│   ├── cadres.json                   # SSS & ISS competency matrices
│   ├── courses.json                  # iGOT + NSSTA catalog
│   ├── manuals/mospi_corpus.json     # Ground truth corpus
│   └── datasets/synthetic_plfs.json  # NSS 80th Round microdata
├── static/
│   ├── css/design-system.css         # MoSPI Gov Design System
│   ├── js/app.js                     # Client state & interactive controllers
│   └── index.html                    # Master UI Dashboard
├── tests/
│   └── test_models.py                # Automated validation test suite
├── CAPABILITY_MAP.md                 # Capability breakdown
└── SPEC-sih-presentation-readiness.md# This specification
```

## Boundaries
- **Always do:**
  - Maintain zero console errors and zero broken state when switching tabs or cadres.
  - Keep offline fallback data functional so the prototype never fails if the server or internet is interrupted.
  - Run `python -m graphify update .` after modifying source code.
- **Ask first:**
  - Modifying the underlying statistical formulas (e.g. Modified Laspeyres or UPS Major Time Criterion).
  - Introducing heavy native binaries that could fail to load on standard judge laptops.
- **Never do:**
  - Leave unhandled `SyntaxError` or unhandled promise rejections on API calls.
  - Hardcode fragile URLs that break when evaluated on alternate ports (5500, 3000, 8080).

## Success Criteria
1. **Interactive SIH Jury Presentation Tour:** A persistent guide banner at the top with "Next Engine ➔" that takes judges through all 7 tabs sequentially with explanatory notes.
2. **SIH Pitch & Architecture Modal:** A prominent "🏆 SIH 26101 Solution Docket" button that displays the executive pitch, system architecture diagram, MoSPI pain-point resolution, and national impact metrics.
3. **100% Tested & Clean:** Automated test script (`tests/test_models.py`) passes all tests for all 7 engines with zero errors.
4. **Visual & Interactive Polish:** Complete responsive layouts, instant feedback, verified citations, and zero text clumping.
