# Capability Map: SIH 2026 MoSPI Competency AI Platform (ID 26101)

| Module ID | Responsibility | Key ML/AI Technique | Depends On | Status |
|---|---|---|---|:---:|
| `mod-competency` | Cadre benchmarking, self-appraisal NLP vectorization & radar gap scoring | TF-IDF, LSA (SVD), Cosine Similarity | — | ✅ Complete |
| `mod-assessment-qc` | Grounded item generation, Bloom's Taxonomy L1-L4, 3-stage anti-hallucination QC | Token-set overlap, semantic vector spread, QTI 2.1 | `mod-competency` | ✅ Complete |
| `mod-proctoring` | AI Proctoring Trust Engine, CV face/gaze telemetry, anti-AI extension sandbox | Optical & DOM mutation scanner, 3-strike freeze | `mod-assessment-qc` | ✅ Complete |
| `mod-pathway` | Blended learning recommender coupling iGOT digital modules with NSSTA residential labs | Constraint-satisfaction graph, Karmayogi credits | `mod-competency` | ✅ Complete |
| `mod-decay` | Skill retention decay over time & methodology drift shock alert system | Exponential decay $S(t) = S_0 e^{-\lambda t}$ | `mod-competency` | ✅ Complete |
| `mod-analytics` | Divisional capability heatmaps (FOD, SDRD, NAD, ESD, DIID) & survey forecaster | Matrix aggregation, predictive readiness index | `mod-competency` | ✅ Complete |
| `mod-virtual-lab` | In-browser Python/Pandas survey microdata engine on synthetic NSS 80th Round | AST execution sandbox, multiplier verification | `mod-competency` | ✅ Complete |
| `mod-knowledge-graph` | 5-Lane Semantic Knowledge Pipeline & interactive pathway traversal | Graphify ontology, BFS pathway highlighting | All modules | ✅ Complete |
| `mod-sih-pitch-deck` | Interactive Jury Guided Tour, SIH Architecture Modal, and Pitch Presentation Docket | Guided walkthrough UI, exportable deck | All modules | 🚀 In Progress |

Build & Presentation Order:
`mod-competency` ➔ `mod-assessment-qc` ➔ `mod-proctoring` ➔ `mod-pathway` ➔ `mod-decay` ➔ `mod-analytics` ➔ `mod-virtual-lab` ➔ `mod-knowledge-graph` ➔ `mod-sih-pitch-deck`
