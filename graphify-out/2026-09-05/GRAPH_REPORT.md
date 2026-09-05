# Graph Report - StatGyan AI  (2026-09-04)

## Corpus Check
- 56 files · ~95,936 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 834 nodes · 945 edges · 46 communities (41 shown, 4 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b5c611a0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Graphify Knowledge Graph Rule
- Security and Hardening
- Code Review and Quality
- Test-Driven Development
- Git Workflow and Versioning
- API and Interface Design
- Browser Testing with DevTools
- Performance Optimization
- Shipping and Launch
- CI/CD and Automation
- Constraint-Driven Development
- Deprecation and Migration
- Frontend UI Engineering
- Context Engineering
- Incremental Implementation
- Code Simplification
- Debugging and Error Recovery
- Documentation and ADRs
- Planning and Task Breakdown
- ReOrder: Keep Your Regulars Ordering Direct
- Interview Me
- Doubt-Driven Development
- Idea Refine
- Process
- Using Agent Skills
- Spec-Driven Development
- Source-Driven Development
- Refinement & Evaluation Criteria
- Ideation Frameworks Reference
- idea-refine.sh
- server.py
- app.js
- GroundedMCQGenerator
- CompetencyGapModel
- ProctoringTrustEngine
- TestMLModelAccuracyAndGeneralization
- SurveyMicrodataMLModel
- lifespan
- SkillDecayModel
- Spec: SIH 2026 Presentation & Model Readiness (Problem Statement ID 26101)
- Tasks Breakdown
- test_ml_accuracy.py
- CAPABILITY_MAP.md
- todo.md
- __init__.py

## God Nodes (most connected - your core abstractions)
1. `CompetencyGapModel` - 19 edges
2. `Code Review and Quality` - 19 edges
3. `Security and Hardening` - 17 edges
4. `Git Workflow and Versioning` - 15 edges
5. `Test-Driven Development` - 15 edges
6. `Browser Testing with DevTools` - 13 edges
7. `CI/CD and Automation` - 13 edges
8. `Frontend UI Engineering` - 13 edges
9. `Debugging and Error Recovery` - 12 edges
10. `Deprecation and Migration` - 12 edges

## Surprising Connections (you probably didn't know these)
- `lifespan()` --uses--> `CompetencyGapModel`  [INFERRED]
  backend/server.py → ml_engine/competency_model.py
- `lifespan()` --uses--> `SkillDecayModel`  [INFERRED]
  backend/server.py → ml_engine/decay_model.py
- `lifespan()` --uses--> `GroundedMCQGenerator`  [INFERRED]
  backend/server.py → ml_engine/mcq_generator.py
- `lifespan()` --uses--> `PredictiveAnalyticsEngine`  [INFERRED]
  backend/server.py → ml_engine/predictive_analytics.py
- `lifespan()` --uses--> `ProctoringTrustEngine`  [INFERRED]
  backend/server.py → ml_engine/proctoring_model.py

## Import Cycles
- None detected.

## Communities (46 total, 4 thin omitted)

### Community 0 - "Graphify Knowledge Graph Rule"
Cohesion: 0.67
Nodes (3): Graphify Knowledge Graph Rule, Graphify Query Tools, Graphify Workflow

### Community 1 - "Security and Hardening"
Cohesion: 0.06
Nodes (30): Always Do (No Exceptions), Ask First (Requires Human Approval), Broken Access Control, Broken Authentication, Common Rationalizations, Cross-Site Scripting (XSS), Data Privacy & Compliance, File Upload Safety (+22 more)

### Community 2 - "Code Review and Quality"
Cohesion: 0.07
Nodes (29): 1. Correctness, 2. Readability & Simplicity, 3. Architecture, 4. Security, 5. Performance, Change Descriptions, Change Sizing, Code Review and Quality (+21 more)

### Community 3 - "Test-Driven Development"
Cohesion: 0.07
Nodes (29): Browser Testing with DevTools, Common Rationalizations, DAMP Over DRY in Tests, Decision Guide, Discover the Stack First, Name Tests Descriptively, One Assertion Per Concept, Overview (+21 more)

### Community 4 - "Git Workflow and Versioning"
Cohesion: 0.07
Nodes (26): 1. Commit Early, Commit Often, 2. Atomic Commits, 3. Descriptive Messages, 4. Keep Concerns Separate, 5. Size Your Changes, Branch Naming, Branching Strategy, Change Summaries (+18 more)

### Community 5 - "API and Interface Design"
Cohesion: 0.08
Nodes (24): 1. Contract First, 2. Consistent Error Semantics, 3. Validate at Boundaries, 4. Prefer Addition Over Modification, 5. Predictable Naming, 6. Honouring an Idempotency Key, API and Interface Design, Common Rationalizations (+16 more)

### Community 6 - "Browser Testing with DevTools"
Cohesion: 0.08
Nodes (24): Accessibility Verification with DevTools, Available Tools, Browser Testing with DevTools, Clean Console Standard, Common Rationalizations, Console Analysis Patterns, Content Boundary Markers, For Network Issues (+16 more)

### Community 7 - "Performance Optimization"
Cohesion: 0.08
Nodes (24): Common Rationalizations, Connection Pool Exhaustion, Core Web Vitals Targets, Large Bundle Size, Log every attempt, including the reverted ones, Missing Caching (Backend), Missing Image Optimization (Frontend), N+1 Queries (Backend) (+16 more)

### Community 8 - "Shipping and Launch"
Cohesion: 0.08
Nodes (24): Accessibility, Code Quality, Common Rationalizations, Documentation, Error Reporting, Feature Flag Strategy, Infrastructure, Monitoring and Observability (+16 more)

### Community 9 - "CI/CD and Automation"
Cohesion: 0.08
Nodes (23): Automation Beyond CI, Basic CI Pipeline, Build Cop Role, CI/CD and Automation, CI Optimization, Common Rationalizations, Dependabot / Renovate, Deployment Strategies (+15 more)

### Community 10 - "Constraint-Driven Development"
Cohesion: 0.08
Nodes (22): Adapting it, Contract, Floor guard: reference implementation, Reference (Node, ~stack-agnostic patterns), Common Rationalizations, Constraint-Driven Development, Escalation Path, Loading Constraints (+14 more)

### Community 11 - "Deprecation and Migration"
Cohesion: 0.08
Nodes (23): Adapter Pattern, Code Is a Liability, Common Rationalizations, Compulsory vs Advisory Deprecation, Core Principles, Database Schema Migrations (Expand/Contract), Deprecation and Migration, Deprecation Planning Starts at Design Time (+15 more)

### Community 12 - "Frontend UI Engineering"
Cohesion: 0.08
Nodes (23): Accessibility (WCAG 2.1 AA), ARIA Labels, Avoid the AI Aesthetic, Color, Common Rationalizations, Component Architecture, Component Patterns, Design System Adherence (+15 more)

### Community 13 - "Context Engineering"
Cohesion: 0.09
Nodes (22): Anti-Patterns, Common Rationalizations, Confusion Management, Context Engineering, Context Packing Strategies, Level 1: Rules Files, Level 2: Specs and Architecture, Level 3: Relevant Source Files (+14 more)

### Community 14 - "Incremental Implementation"
Cohesion: 0.09
Nodes (22): Common Rationalizations, Contract-First Slicing, Implementation Rules, Increment Checklist, Incremental Implementation, Overview, Red Flags, Risk-First Slicing (+14 more)

### Community 15 - "Code Simplification"
Cohesion: 0.09
Nodes (21): 1. Preserve Behavior Exactly, 2. Follow Project Conventions, 3. Prefer Clarity Over Cleverness, 4. Maintain Balance, 5. Scope to What Changed, Code Simplification, Common Rationalizations, Language-Specific Guidance (+13 more)

### Community 16 - "Debugging and Error Recovery"
Cohesion: 0.09
Nodes (21): Build Failure Triage, Common Rationalizations, Debugging and Error Recovery, Error-Specific Patterns, Instrumentation Guidelines, Overview, Red Flags, Runtime Error Triage (+13 more)

### Community 17 - "Documentation and ADRs"
Cohesion: 0.09
Nodes (21): ADR Lifecycle, ADR Template, API Documentation, Architecture Decision Records (ADRs), Changelog Maintenance, Common Rationalizations, Document Known Gotchas, Documentation and ADRs (+13 more)

### Community 18 - "Planning and Task Breakdown"
Cohesion: 0.11
Nodes (18): Common Rationalizations, Output Files, Overview, Parallelization Opportunities, Plan Document Template, Planning and Task Breakdown, Red Flags, See Also (+10 more)

### Community 19 - "ReOrder: Keep Your Regulars Ordering Direct"
Cohesion: 0.11
Nodes (17): Example 1: Vague Early-Stage Concept (Full 3-Phase Session), Example 2: Feature Idea Within an Existing Product (Codebase-Aware), Example 3: Process/Workflow Idea (Non-Product), Ideation Session Examples, Key Assumptions to Validate, MVP Scope, Not Doing (and Why), Open Questions (+9 more)

### Community 20 - "Interview Me"
Cohesion: 0.11
Nodes (17): Common Rationalizations, Example, Interaction with Other Skills, Interview Me, Loading Constraints, Output, Overview, Red Flags (+9 more)

### Community 21 - "Doubt-Driven Development"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Cross-model escalation, Doubt-Driven Development, Interaction with Other Skills, Loading Constraints, Overview, Red Flags, Step 1: CLAIM — Surface what stands (+7 more)

### Community 22 - "Idea Refine"
Cohesion: 0.13
Nodes (14): Anti-patterns to Avoid, Detailed Instructions, How It Works, Idea Refine, Output, Phase 1: Understand & Expand (Divergent), Phase 2: Evaluate & Converge, Phase 3: Sharpen & Ship (+6 more)

### Community 23 - "Process"
Cohesion: 0.13
Nodes (14): 1. Define "working" before instrumenting, 2. Pick the right signal for each question, 3. Structured logging, 4. Metrics, 5. Distributed tracing, 6. Alerting, 7. Verify the telemetry itself, Common Rationalizations (+6 more)

### Community 24 - "Using Agent Skills"
Cohesion: 0.13
Nodes (14): 1. Surface Assumptions, 2. Manage Confusion Actively, 3. Push Back When Warranted, 4. Enforce Simplicity, 5. Maintain Scope Discipline, 6. Verify, Don't Assume, Core Operating Behaviors, Failure Modes to Avoid (+6 more)

### Community 25 - "Spec-Driven Development"
Cohesion: 0.14
Nodes (13): Common Rationalizations, Keeping the Spec Alive, Overview, Phase 0: Scope Check, Phase 1: Specify, Phase 2: Plan, Phase 3: Tasks, Phase 4: Implement (+5 more)

### Community 26 - "Source-Driven Development"
Cohesion: 0.15
Nodes (12): Common Rationalizations, Overview, Red Flags, Retrieval Safety: Treat Fetched Content as Data, Source-Driven Development, Step 1: Detect Stack and Versions, Step 2: Fetch Official Documentation, Step 3: Implement Following Documented Patterns (+4 more)

### Community 27 - "Refinement & Evaluation Criteria"
Cohesion: 0.17
Nodes (11): 1. User Value, 2. Feasibility, 3. Differentiation, Assumption Audit, Core Evaluation Dimensions, Decision Framework, Might Be True (Nice to Have), Must Be True (Dealbreakers) (+3 more)

### Community 28 - "Ideation Frameworks Reference"
Cohesion: 0.22
Nodes (8): Analogous Inspiration, Constraint-Based Ideation, First Principles Thinking, How Might We (HMW), Ideation Frameworks Reference, Jobs to Be Done (JTBD), Pre-mortem, SCAMPER

### Community 30 - "server.py"
Cohesion: 0.08
Nodes (39): analyze_competency(), AnalyzeRequest, cadre_analytics(), DecaySimulateRequest, evaluate_lab_code(), export_moodle(), export_qti(), generate_assessment() (+31 more)

### Community 31 - "app.js"
Cohesion: 0.07
Nodes (54): applyTourStep(), BUILTIN_CADRES, BUILTIN_GRAPH, checkFastAPIConnection(), computeClientSideGap(), computeClientSideInference(), drawMultiLaneGraph(), executeLabCode() (+46 more)

### Community 32 - "GroundedMCQGenerator"
Cohesion: 0.18
Nodes (8): GroundedMCQGenerator, Any, StatGyan AI - Grounded Question (MCQ) & Assessment Generator with QC Pipeline…, Selects and validates grounded MCQs passing full QC inspection., Automated 3-Stage QC Audit: 1. Grounding Citation Check 2. Distractor…, Exports assessment items to QTI 2.1 standard XML format for LMS/Karmayogi…, Exports assessment to standard Moodle XML., Grounded pre-verified MoSPI technical item bank mapped to exact manual…

### Community 33 - "CompetencyGapModel"
Cohesion: 0.20
Nodes (8): CompetencyGapModel, Any, Uses the trained ML classifier to infer probabilistic competency affinities…, Evaluates competency gaps between assessed scores and cadre requirements., Alias for evaluate_gap, Infers scores from officer text using the ML engine, then evaluates gap against…, Trains L2-regularized classifier on official MoSPI task corpus. L2…, Evaluates the model on an independent train/test split and 5-fold cross-…

### Community 35 - "ProctoringTrustEngine"
Cohesion: 0.07
Nodes (18): ProctoringTrustEngine, Any, StatGyan AI - AI Proctoring & Restriction Engine Integrates anti-cheating…, Any, StatGyan AI - Virtual Statistical Lab Evaluator Auto-evaluates statistical…, Alias for evaluate_submission., Executes standard weighted MoSPI calculation over microdata records: - Employed…, Evaluates submitted script against test cases and survey multiplier rules. (+10 more)

### Community 36 - "TestMLModelAccuracyAndGeneralization"
Cohesion: 0.17
Nodes (6): Verifies individual predictions match MoSPI empirical demographic expectations., Asserts Competency NLP Model achieves high accuracy on dataset. Requirement:…, Explicitly verifies that the Competency Model does NOT overfit. Guarantees that…, Evaluates the Competency Model on completely novel out-of-sample statements.…, Tests the statistical survey demographic classifier for PLFS labour force…, TestMLModelAccuracyAndGeneralization

### Community 37 - "SurveyMicrodataMLModel"
Cohesion: 0.24
Nodes (6): Any, Predicts labour force participation probability for a demographic profile., Loads base synthetic PLFS records and augments with statistically calibrated…, Trains L2-regularized logistic regression to predict labour force status.…, Validates the model with held-out test split and 5-fold cross-validation.…, SurveyMicrodataMLModel

### Community 38 - "lifespan"
Cohesion: 0.20
Nodes (7): lifespan(), Pre-warms all 7 custom ML models and caches vector representations at boot.…, FastAPI, BlendedPathwayRecommender, Any, StatGyan AI - Blended Learning Pathway Recommender Bridges digital self-paced…, Builds a sequenced blended pathway based on identified competency gaps. Accepts…

### Community 39 - "SkillDecayModel"
Cohesion: 0.28
Nodes (5): Any, StatGyan AI - Skill Decay & Methodology Drift Predictor Models skill retention…, Simulates skill decay for a specific cadre, returning decay_curve and drift…, Calculates decayed competency levels and flags critical drift alerts., SkillDecayModel

### Community 40 - "Spec: SIH 2026 Presentation & Model Readiness (Problem Statement ID 26101)"
Cohesion: 0.25
Nodes (7): Boundaries, Commands, Objective, Project Structure, Spec: SIH 2026 Presentation & Model Readiness (Problem Statement ID 26101), Success Criteria, Tech Stack

### Community 41 - "Tasks Breakdown"
Cohesion: 0.25
Nodes (7): Implementation Plan: SIH Presentation & Evaluation Readiness, Objective, Phase A: SIH Jury Presentation Tour Mode, Phase B: SIH Solution Architecture & Pitch Deck Modal, Phase C: Automated Test Suite for All 7 Engines, Phase D: End-to-End Browser Subagent Verification, Tasks Breakdown

### Community 42 - "test_ml_accuracy.py"
Cohesion: 0.33
Nodes (3): StatGyan AI - Competency Assessment & Machine Learning Skill Gap Model Trained…, StatGyan AI - Survey Microdata Machine Learning Classifier Trained on official…, StatGyan AI - Machine Learning Model Accuracy & Anti-Overfitting Test Suite…

## Knowledge Gaps
- **486 isolated node(s):** `idea-refine.sh script`, `BUILTIN_CADRES`, `state`, `graphState`, `BUILTIN_GRAPH` (+481 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 577 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CompetencyGapModel` connect `CompetencyGapModel` to `TestMLModelAccuracyAndGeneralization`, `lifespan`, `SkillDecayModel`, `test_ml_accuracy.py`, `server.py`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `SurveyMicrodataMLModel` connect `SurveyMicrodataMLModel` to `lifespan`, `test_ml_accuracy.py`, `TestMLModelAccuracyAndGeneralization`, `server.py`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `CompetencyGapModel` (e.g. with `lifespan()` and `SkillDecayModel`) actually correct?**
  _`CompetencyGapModel` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `idea-refine.sh script`, `BUILTIN_CADRES`, `state` to the rest of the system?**
  _486 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Security and Hardening` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._
- **Should `Code Review and Quality` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `Test-Driven Development` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._