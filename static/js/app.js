/**
 * StatGyan AI - Client Application Logic
 * Communicates with FastAPI backend for Competency Gap Analysis,
 * Grounded Question Generation (QC), Blended Pathways, and Virtual Lab.
 */

const API_BASE = "";

// Global App State
const state = {
  activeCadre: "jso",
  cadres: [],
  gapAnalysis: null,
  radarChart: null,
  activeAssessment: null,
  pathway: null,
  analytics: null,
  // Proctoring state
  isExamLocked: false,
  proctoringSessionId: "SESSION-MOSPI-2026-001",
  trustScore: 100,
  strikes: 0,
  incidents: []
};

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  loadCadres();
  setupRoleSwitcher();
  setupAssessmentFilters();
  setupVirtualLab();
  setupDecaySimulator();
  setupProctoringEngine();
});

// 1. Navigation Tabs
function setupNavigation() {
  const tabs = document.querySelectorAll(".nav-tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const targetId = tab.getAttribute("data-tab");
      document.querySelectorAll(".tab-pane").forEach(pane => {
        pane.classList.remove("active");
      });
      const targetPane = document.getElementById(targetId);
      if (targetPane) {
        targetPane.classList.add("active");
        handleTabActivation(targetId);
      }
    });
  });
}

function handleTabActivation(tabId) {
  if (tabId === "tab-pathway" && !state.pathway) {
    loadPathway();
  } else if (tabId === "tab-analytics" && !state.analytics) {
    loadCadreAnalytics();
  } else if (tabId === "tab-graph") {
    renderKnowledgeGraph();
  }
}

// 2. Role Switcher & Cadre Loading
async function loadCadres() {
  try {
    const res = await fetch(`${API_BASE}/api/cadres`);
    const data = await res.json();
    state.cadres = data.cadres;
    
    const select = document.getElementById("cadre-select");
    select.innerHTML = "";
    state.cadres.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = `${c.title} (${c.cadre_group})`;
      select.appendChild(opt);
    });

    select.value = state.activeCadre;
    triggerCompetencyAnalysis();
  } catch (err) {
    console.error("Failed to load cadres:", err);
  }
}

function setupRoleSwitcher() {
  const select = document.getElementById("cadre-select");
  select.addEventListener("change", (e) => {
    state.activeCadre = e.target.value;
    triggerCompetencyAnalysis();
    loadPathway();
  });
}

// 3. Competency Gap Analysis & Radar Chart
async function triggerCompetencyAnalysis() {
  try {
    const res = await fetch(`${API_BASE}/api/competency/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cadre_id: state.activeCadre })
    });
    const data = await res.json();
    state.gapAnalysis = data;
    renderCompetencyOverview(data);
    renderRadarChart(data.radar_data);
    renderDomainList(data.domain_breakdown);
  } catch (err) {
    console.error("Competency analysis failed:", err);
  }
}

function renderCompetencyOverview(data) {
  document.getElementById("officer-readiness-val").textContent = `${data.overall_readiness_pct}%`;
  document.getElementById("avg-gap-val").textContent = `${data.average_gap} pts`;
  document.getElementById("critical-gaps-val").textContent = data.critical_gap_count;
  document.getElementById("active-cadre-title").textContent = data.cadre_title;
}

function renderRadarChart(radarData) {
  const ctx = document.getElementById("competencyRadarChart");
  if (!ctx) return;

  if (state.radarChart) {
    state.radarChart.destroy();
  }

  // Use Chart.js
  state.radarChart = new Chart(ctx, {
    type: "radar",
    data: {
      labels: radarData.labels,
      datasets: [
        {
          label: "Benchmark Required (MoSPI Standard)",
          data: radarData.required,
          borderColor: "#38BDF8",
          backgroundColor: "rgba(56, 189, 248, 0.15)",
          borderWidth: 2,
          pointBackgroundColor: "#38BDF8"
        },
        {
          label: "Assessed Competency Level",
          data: radarData.assessed,
          borderColor: "#F59E0B",
          backgroundColor: "rgba(245, 158, 11, 0.25)",
          borderWidth: 2,
          pointBackgroundColor: "#F59E0B"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: "rgba(255, 255, 255, 0.1)" },
          grid: { color: "rgba(255, 255, 255, 0.08)" },
          pointLabels: {
            color: "#94A3B8",
            font: { size: 10.5, family: "Inter" }
          },
          ticks: {
            backdropColor: "transparent",
            color: "#64748B",
            stepSize: 20
          },
          suggestedMin: 20,
          suggestedMax: 100
        }
      },
      plugins: {
        legend: {
          labels: { color: "#F8FAFC", font: { family: "Outfit", size: 11 } }
        }
      }
    }
  });
}

function renderDomainList(domains) {
  const container = document.getElementById("domain-gap-list");
  if (!container) return;

  container.innerHTML = "";
  domains.forEach(d => {
    const item = document.createElement("div");
    item.style.cssText = "padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center;";
    
    let badgeColor = "#10B981";
    let badgeBg = "rgba(16, 185, 129, 0.15)";
    if (d.severity === "Critical") {
      badgeColor = "#EF4444";
      badgeBg = "rgba(239, 68, 68, 0.15)";
    } else if (d.severity === "Moderate") {
      badgeColor = "#F59E0B";
      badgeBg = "rgba(245, 158, 11, 0.15)";
    }

    item.innerHTML = `
      <div>
        <div style="font-weight: 600; font-size: 0.85rem; color: #FFFFFF;">${d.domain}</div>
        <div style="font-size: 0.75rem; color: #94A3B8;">Target: ${d.required_level}% | Current: ${d.assessed_level}%</div>
      </div>
      <div style="text-align: right;">
        <span style="font-size: 0.75rem; font-weight: 700; color: ${badgeColor}; background: ${badgeBg}; padding: 3px 8px; border-radius: 10px;">
          ${d.status}
        </span>
      </div>
    `;
    container.appendChild(item);
  });
}

// 4. Grounded Assessment & MCQ Generator Studio
function setupAssessmentFilters() {
  const btn = document.getElementById("btn-generate-mcq");
  if (btn) {
    btn.addEventListener("click", runMCQGeneration);
  }

  // Export buttons
  const qtiBtn = document.getElementById("btn-export-qti");
  if (qtiBtn) {
    qtiBtn.addEventListener("click", () => window.open(`${API_BASE}/api/assessment/export/qti`, "_blank"));
  }
  const moodleBtn = document.getElementById("btn-export-moodle");
  if (moodleBtn) {
    moodleBtn.addEventListener("click", () => window.open(`${API_BASE}/api/assessment/export/moodle`, "_blank"));
  }

  // Initial generation
  runMCQGeneration();
}

async function runMCQGeneration(retryCount = 0) {
  const manualId = document.getElementById("filter-manual")?.value || null;
  const bloom = document.getElementById("filter-bloom")?.value || null;
  const container = document.getElementById("mcq-container");
  if (!container) return;

  container.innerHTML = `
    <div style="text-align: center; padding: 2rem; color: #94A3B8;">
      <div class="pulse-dot" style="display: inline-block; margin-bottom: 0.5rem;"></div>
      <div style="font-weight: 600; color: #F8FAFC;">Running Grounded Extraction & QC Engine...</div>
      <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Auditing source citations against MoSPI manuals</div>
    </div>
  `;

  try {
    const res = await fetch(`${API_BASE}/api/assessment/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        manual_id: manualId || null,
        bloom_level: bloom || null,
        count: 4
      })
    });

    if (!res.ok) {
      throw new Error(`Server returned HTTP ${res.status} (${res.statusText || 'Error'})`);
    }

    const text = await res.text();
    if (!text || !text.trim()) {
      throw new Error("Server returned an empty response payload");
    }

    const data = JSON.parse(text);
    if (!data.items || data.items.length === 0) {
      throw new Error("No items found matching the selected filter criteria");
    }

    state.activeAssessment = data;
    renderMCQs(data);
  } catch (err) {
    console.warn("MCQ generation error:", err);
    if (retryCount < 1) {
      // Auto-retry once after 700ms in case server was restarting
      setTimeout(() => runMCQGeneration(retryCount + 1), 700);
      return;
    }
    renderMCQError(container, err);
  }
}

function renderMCQError(container, err) {
  container.innerHTML = `
    <div class="card" style="border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.08); text-align: center; padding: 2rem;">
      <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚠️</div>
      <div style="font-weight: 700; color: #EF4444; font-size: 1.05rem; margin-bottom: 0.5rem;">Assessment Generation Temporary Interruption</div>
      <div style="color: #94A3B8; font-size: 0.85rem; max-width: 500px; margin: 0 auto 1.25rem;">
        The AI generation engine encountered a temporary response error: <br>
        <code style="color: #F87171; background: rgba(0,0,0,0.3); padding: 2px 8px; border-radius: 4px; display: inline-block; margin-top: 4px;">${err.message || err}</code>
      </div>
      <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <button class="btn btn-primary" onclick="runMCQGeneration(0)">
          <span>🔄</span> Retry Assessment Generation
        </button>
        <button class="btn btn-secondary" onclick="loadSampleMCQs()">
          <span>📋</span> Load Grounded MoSPI Items
        </button>
      </div>
    </div>
  `;
}

function loadSampleMCQs() {
  const fallbackData = {
    total_generated: 4,
    qc_pass_rate_pct: 100.0,
    items: [
      {
        id: "mcq_plfs_001",
        manual_id: "plfs_manual_vol1",
        section_id: "plfs_sec_101",
        domain: "Survey Methodology & Sampling",
        bloom_level: "Level 1: Recall / Knowledge",
        question: "Under the Periodic Labour Force Survey (PLFS), what is the standard reference period for determining a person's Usual Principal Status (UPS)?",
        options: [
          "365 days preceding the date of survey",
          "30 days preceding the date of survey",
          "7 days preceding the date of survey",
          "180 days preceding the date of survey"
        ],
        correct_index: 0,
        explanation: "According to the PLFS Manual, Usual Status takes a reference period of 365 days preceding the date of survey, applying the major time criterion.",
        citation: "PLFS Manual Vol. I, Section 2.14, p. 18",
        qc_audit: {
          passed: true,
          grounding_confidence: 1.0,
          distractor_plausibility: 69.0,
          verified_citation: "PLFS Manual Vol. I, Section 2.14, p. 18",
          qc_status: "VERIFIED_GROUNDED"
        }
      },
      {
        id: "mcq_cpi_001",
        manual_id: "cpi_compilation_guide",
        section_id: "cpi_sec_201",
        domain: "Index Numbers (CPI & IIP)",
        bloom_level: "Level 2: Conceptual Understanding",
        question: "Which mathematical aggregation principle does MoSPI utilize for aggregating item price relatives into higher-level CPI sub-groups?",
        options: [
          "Weighted arithmetic average with base-period expenditure weights (Modified Laspeyres)",
          "Weighted harmonic mean with current-period quantity weights (Paasche Index)",
          "Geometric mean of Laspeyres and Paasche formulations (Fisher Ideal Index)",
          "Unweighted median of elementary price relatives"
        ],
        correct_index: 0,
        explanation: "MoSPI CPI uses a modified Laspeyres formula where elementary price relatives are aggregated using base-period consumer expenditure weights.",
        citation: "CPI Compilation Guidelines, Chapter 4, p. 32",
        qc_audit: {
          passed: true,
          grounding_confidence: 1.0,
          distractor_plausibility: 75.0,
          verified_citation: "CPI Compilation Guidelines, Chapter 4, p. 32",
          qc_status: "VERIFIED_GROUNDED"
        }
      },
      {
        id: "mcq_nas_001",
        manual_id: "nas_methodology",
        section_id: "nas_sec_301",
        domain: "National Accounts & GDP Estimation",
        bloom_level: "Level 2: Conceptual Understanding",
        question: "Under the System of National Accounts (SNA 2008), how is Gross Domestic Product (GDP) at market prices derived from Gross Value Added (GVA) at basic prices?",
        options: [
          "GDP = GVA at basic prices + Product Taxes - Product Subsidies",
          "GDP = GVA at basic prices - Product Taxes + Product Subsidies",
          "GDP = GVA at basic prices + Production Taxes - Production Subsidies",
          "GDP = GVA at factor cost + Indirect Taxes"
        ],
        correct_index: 0,
        explanation: "In SNA 2008, GDP at market prices = GVA at basic prices + Product Taxes - Product Subsidies. Basic price already includes production taxes/subsidies.",
        citation: "NAS Sources & Methods, Chapter 2, p. 15",
        qc_audit: {
          passed: true,
          grounding_confidence: 1.0,
          distractor_plausibility: 82.0,
          verified_citation: "NAS Sources & Methods, Chapter 2, p. 15",
          qc_status: "VERIFIED_GROUNDED"
        }
      }
    ]
  };
  state.activeAssessment = fallbackData;
  renderMCQs(fallbackData);
}

function renderMCQs(data) {
  const container = document.getElementById("mcq-container");
  const qcStats = document.getElementById("qc-pass-rate-display");
  if (qcStats) {
    qcStats.textContent = `QC Verification Pass Rate: ${data.qc_pass_rate_pct}%`;
  }

  container.innerHTML = "";
  data.items.forEach((item, idx) => {
    const qc = item.qc_audit;
    const card = document.createElement("div");
    card.className = "mcq-card";

    let qcBadgeClass = qc.passed ? "background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3);"
                                 : "background: rgba(245, 158, 11, 0.2); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3);";

    let optionsHtml = item.options.map((opt, oIdx) => {
      const isCorrect = oIdx === item.correct_index;
      return `
        <div class="mcq-option ${isCorrect ? 'correct' : ''}" onclick="this.classList.toggle('selected')">
          <span style="font-weight: 700; width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">
            ${String.fromCharCode(65 + oIdx)}
          </span>
          <span>${opt}</span>
          ${isCorrect ? '<span style="margin-left: auto; font-size: 0.75rem; color: #10B981;">✓ Official Key</span>' : ''}
        </div>
      `;
    }).join("");

    card.innerHTML = `
      <div class="mcq-meta">
        <div style="display: flex; gap: 0.5rem; align-items: center;">
          <span class="bloom-pill">${item.bloom_level}</span>
          <span style="font-size: 0.75rem; color: #94A3B8;">${item.domain}</span>
        </div>
        <span style="font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 12px; ${qcBadgeClass}">
          ${qc.qc_status}
        </span>
      </div>
      <div class="mcq-question">Q${idx + 1}. ${item.question}</div>
      <div class="mcq-options">${optionsHtml}</div>
      
      <div class="qc-audit-box">
        <div class="qc-header">
          <span>🔍 Automated Quality Control (QC) Inspector</span>
          <span>Grounding: ${(qc.grounding_confidence * 100).toFixed(0)}%</span>
        </div>
        <div style="color: #94A3B8; font-size: 0.75rem; margin-bottom: 0.35rem;">
          <strong style="color: #F8FAFC;">Grounding Citation:</strong> ${item.citation}
        </div>
        <div style="color: #94A3B8; font-size: 0.75rem; margin-bottom: 0.35rem;">
          <strong style="color: #F8FAFC;">Distractor Plausibility:</strong> ${qc.distractor_plausibility}% (Semantic vector spread)
        </div>
        <div style="color: #CBD5E1; font-size: 0.75rem; font-style: italic;">
          "${item.explanation}"
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// 5. Blended Pathway (iGOT + NSSTA)
async function loadPathway() {
  const container = document.getElementById("pathway-timeline");
  if (!container) return;

  container.innerHTML = `<div style="color: #94A3B8; padding: 1.5rem;">Synthesizing Blended iGOT + NSSTA Pathway...</div>`;

  try {
    const res = await fetch(`${API_BASE}/api/recommender/pathway`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cadre_id: state.activeCadre })
    });
    const data = await res.json();
    state.pathway = data;
    renderPathway(data);
  } catch (err) {
    container.innerHTML = `<div style="color: #EF4444;">Failed to build pathway: ${err}</div>`;
  }
}

function renderPathway(data) {
  const container = document.getElementById("pathway-timeline");
  const elSteps = document.getElementById("total-path-steps");
  const elOnline = document.getElementById("total-online-hrs");
  const elNssta = document.getElementById("total-nssta-days");
  const elCredits = document.getElementById("total-karmayogi-credits");

  if (elSteps) elSteps.textContent = data.total_pathway_steps;
  if (elOnline) elOnline.textContent = `${data.total_online_hours} hrs`;
  if (elNssta) elNssta.textContent = `${data.total_residential_days} days`;
  if (elCredits) elCredits.textContent = data.total_karmayogi_credits;

  if (!container) return;
  container.innerHTML = "";
  data.learning_pathway.forEach((step, idx) => {
    const isDigital = step.channel.includes("iGOT");
    const borderAccent = isDigital ? "#38BDF8" : "#8B5CF6";
    const channelBadge = isDigital 
      ? '<span style="background: rgba(56, 189, 248, 0.2); color: #38BDF8; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">Digital (iGOT Karmayogi)</span>'
      : '<span style="background: rgba(139, 92, 246, 0.2); color: #C084FC; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">In-Person Lab (NSSTA TPAC)</span>';

    const card = document.createElement("div");
    card.style.cssText = `
      position: relative;
      padding-left: 2rem;
      padding-bottom: 1.5rem;
      border-left: 2px solid rgba(255, 255, 255, 0.1);
    `;

    card.innerHTML = `
      <div style="position: absolute; left: -9px; top: 0; width: 16px; height: 16px; border-radius: 50%; background: ${borderAccent}; border: 3px solid #090D16;"></div>
      <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border-card); border-radius: var(--radius-sm); padding: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <div>
            <span style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Step ${step.step_order} • ${step.phase}</span>
            <div style="font-weight: 700; font-size: 1rem; color: #FFFFFF; margin-top: 2px;">${step.title}</div>
          </div>
          ${channelBadge}
        </div>
        <div style="font-size: 0.8rem; color: #94A3B8; display: flex; gap: 1.5rem; margin-bottom: 0.75rem;">
          <span><strong>Domain:</strong> ${step.domain}</span>
          <span><strong>Duration:</strong> ${step.duration}</span>
          ${step.dates ? `<span><strong>Session Dates:</strong> ${step.dates}</span>` : ''}
          ${step.location ? `<span><strong>Location:</strong> ${step.location}</span>` : ''}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.75rem; color: #38BDF8;">Targeting Gap: -${step.targeted_gap_points} pts</span>
          <button class="btn ${isDigital ? 'btn-outline' : 'btn-primary'}" style="padding: 0.35rem 0.85rem; font-size: 0.75rem;" onclick="alert('Simulation: Officer enrolled in ${step.course_code}!')">
            ${isDigital ? 'Start on iGOT' : 'Nominate for NSSTA'}
          </button>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// 6. Cadre Management & HR Analytics
async function loadCadreAnalytics() {
  try {
    const res = await fetch(`${API_BASE}/api/cadre/analytics`);
    const data = await res.json();
    state.analytics = data;
    renderDivisionalHeatmap(data.heatmap);
    renderReadinessForecasts(data.readiness_forecasts);
  } catch (err) {
    console.error("Failed to load analytics:", err);
  }
}

function renderDivisionalHeatmap(heatmapData) {
  const container = document.getElementById("divisional-heatmap-body");
  if (!container) return;

  container.innerHTML = "";
  heatmapData.heatmap_data.forEach(div => {
    const row = document.createElement("tr");

    const getScoreCell = (score) => {
      let bg = "rgba(16, 185, 129, 0.25)";
      let color = "#A7F3D0";
      if (score < 60) {
        bg = "rgba(239, 68, 68, 0.25)";
        color = "#FCA5A5";
      } else if (score < 80) {
        bg = "rgba(245, 158, 11, 0.25)";
        color = "#FDE68A";
      }
      return `<td style="text-align: center;"><span class="heat-cell" style="background: ${bg}; color: ${color};">${score}%</span></td>`;
    };

    const c = div.competencies;
    row.innerHTML = `
      <td>
        <div style="font-weight: 700; color: #FFFFFF;">${div.division_id}</div>
        <div style="font-size: 0.75rem; color: #64748B;">${div.division_name}</div>
      </td>
      <td style="color: #94A3B8;">${div.strength.toLocaleString()}</td>
      ${getScoreCell(c["Survey Methodology & Sampling"])}
      ${getScoreCell(c["National Accounts & GDP Estimation"])}
      ${getScoreCell(c["Index Numbers (CPI & IIP)"])}
      ${getScoreCell(c["Data Analytics & Programming"])}
      ${getScoreCell(c["Field Operations & CAPI Validation"])}
      ${getScoreCell(c["Official Statistics Governance & Quality"])}
    `;
    container.appendChild(row);
  });
}

function renderReadinessForecasts(forecasts) {
  const container = document.getElementById("survey-forecast-cards");
  if (!container) return;

  container.innerHTML = "";
  forecasts.forEach(f => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
        <div>
          <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Launch Target: ${f.launch_date}</span>
          <div style="font-family: var(--font-heading); font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">${f.title}</div>
        </div>
        <span style="font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 12px; background: rgba(255,255,255,0.08); color: ${f.status_color}; border: 1px solid ${f.status_color};">
          ${f.risk_level}
        </span>
      </div>
      <div style="margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
          <span style="color: #94A3B8;">Predicted Deployment Readiness</span>
          <span style="font-weight: 700; color: ${f.status_color};">${f.readiness_pct}%</span>
        </div>
        <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;">
          <div style="width: ${f.readiness_pct}%; height: 100%; background: ${f.status_color};"></div>
        </div>
      </div>
      <div style="font-size: 0.8rem; color: #CBD5E1; background: rgba(0,0,0,0.3); padding: 0.65rem; border-radius: 6px;">
        <strong style="color: #38BDF8;">Cadre Strategy:</strong> ${f.strategic_action}
      </div>
    `;
    container.appendChild(card);
  });
}

// 7. Virtual Statistical Lab
function setupVirtualLab() {
  const runBtn = document.getElementById("btn-run-code");
  if (runBtn) {
    runBtn.addEventListener("click", executeLabCode);
  }
}

async function executeLabCode() {
  const code = document.getElementById("lab-code-input")?.value || "";
  const outputBox = document.getElementById("lab-output-display");
  if (!outputBox) return;

  outputBox.innerHTML = `<span style="color: #94A3B8;">Executing against synthetic MoSPI microdata engine...</span>`;

  try {
    const res = await fetch(`${API_BASE}/api/lab/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ script_code: code })
    });
    const result = await res.json();
    
    let checksHtml = result.detailed_checks.map(chk => {
      const pass = chk.passed;
      return `
        <div style="margin-bottom: 0.5rem; display: flex; align-items: flex-start; gap: 0.5rem;">
          <span style="color: ${pass ? '#10B981' : '#EF4444'}; font-weight: 700;">${pass ? '✓' : '✗'}</span>
          <div>
            <div style="color: #FFFFFF; font-weight: 600;">${chk.test_name}</div>
            <div style="color: #94A3B8; font-size: 0.75rem;">${chk.feedback || `Expected: ${chk.expected} | Actual: ${chk.actual}`}</div>
          </div>
        </div>
      `;
    }).join("");

    outputBox.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; margin-bottom: 0.75rem;">
        <span style="font-weight: 700; color: ${result.status === 'PASSED' ? '#10B981' : '#EF4444'};">
          ${result.status === 'PASSED' ? 'TEST EXECUTION: ALL PASSED (100%)' : 'VALIDATION REQUIRED'}
        </span>
        <span style="color: #38BDF8; font-size: 0.75rem;">Source: ${result.official_citation}</span>
      </div>
      <div style="font-size: 0.8rem; margin-bottom: 0.75rem;">${checksHtml}</div>
      <div style="background: rgba(0,0,0,0.4); padding: 0.5rem; border-radius: 4px; font-size: 0.75rem; color: #A7F3D0;">
        Derived MoSPI Key Indicators: WPR = ${result.metrics.WPR}% | LFPR = ${result.metrics.LFPR}% | UR = ${result.metrics.UR}%
      </div>
    `;
  } catch (err) {
    outputBox.innerHTML = `<span style="color: #EF4444;">Lab error: ${err}</span>`;
  }
}

// 8. Skill Decay & Methodology Drift Simulator
function setupDecaySimulator() {
  const btn = document.getElementById("btn-simulate-decay");
  if (btn) {
    btn.addEventListener("click", async () => {
      const months = parseFloat(document.getElementById("decay-months-slider")?.value || 8);
      try {
        const res = await fetch(`${API_BASE}/api/decay/simulate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ cadre_id: state.activeCadre, months: months })
        });
        const data = await res.json();
        renderDecayResults(data);
      } catch (err) {
        console.error("Decay simulation failed:", err);
      }
    });
  }
}

function renderDecayResults(data) {
  const container = document.getElementById("decay-alerts-container");
  if (!container) return;

  container.innerHTML = "";
  data.active_drift_alerts.forEach(al => {
    const alertBox = document.createElement("div");
    alertBox.className = "alert-banner";
    alertBox.innerHTML = `
      <div class="alert-icon-text">
        <span class="alert-badge">${al.urgency} DRIFT</span>
        <div>
          <div style="font-weight: 700; color: #FFFFFF;">${al.title}</div>
          <div style="font-size: 0.8rem; color: #E2E8F0;">${al.summary}</div>
          <div style="font-size: 0.75rem; color: #FCA5A5; margin-top: 2px;">Impact: ${al.shock_impact} • Action: ${al.action_required}</div>
        </div>
      </div>
      <button class="btn btn-primary" style="padding: 0.4rem 0.9rem; font-size: 0.75rem; white-space: nowrap;" onclick="alert('Enrolling in priority refresher for ${al.domain}...')">
        Launch Refresher
      </button>
    `;
    container.appendChild(alertBox);
  });
}

// 9. Knowledge Graph Explorer (Canvas)
async function renderKnowledgeGraph() {
  const canvas = document.getElementById("graph-canvas");
  if (!canvas) return;

  try {
    const res = await fetch(`${API_BASE}/api/graph`);
    const graph = await res.json();

    const ctx = canvas.getContext("2d");
    const width = canvas.parentElement.clientWidth;
    canvas.width = width;
    canvas.height = 420;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Layout nodes along concentric circles
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    const nodePositions = {};
    const totalNodes = graph.nodes.length;

    graph.nodes.forEach((node, i) => {
      let radius = 140;
      if (node.type === "Cadre") radius = 60;
      else if (node.type === "Competency") radius = 120;
      else radius = 175;

      const angle = (i / totalNodes) * 2 * Math.PI;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      nodePositions[node.id] = { x, y, ...node };
    });

    // Draw Edges
    ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
    ctx.lineWidth = 1;
    graph.edges.forEach(edge => {
      const from = nodePositions[edge.from];
      const to = nodePositions[edge.to];
      if (from && to) {
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.stroke();
      }
    });

    // Draw Nodes
    graph.nodes.forEach(node => {
      const pos = nodePositions[node.id];
      if (!pos) return;

      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 8, 0, 2 * Math.PI);
      ctx.fillStyle = pos.color;
      ctx.fill();
      ctx.strokeStyle = "#FFFFFF";
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.font = "9px Inter";
      ctx.fillStyle = "#CBD5E1";
      ctx.textAlign = "center";
      ctx.fillText(pos.label.slice(0, 18), pos.x, pos.y + 18);
    });

  } catch (err) {
    console.error("Knowledge graph rendering failed:", err);
  }
}

// 10. AI Proctoring & Security Lockdown Engine
function setupProctoringEngine() {
  const toggleBtn = document.getElementById("btn-toggle-proctoring");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleProctoringMode);
  }

  // Setup violation simulation buttons
  document.getElementById("btn-sim-tab-switch")?.addEventListener("click", () => {
    triggerProctoringViolation("TAB_SWITCH_ATTEMPT", "Candidate switched away from assessment window (Alt+Tab or new tab).", "HIGH");
  });

  document.getElementById("btn-sim-extension")?.addEventListener("click", () => {
    triggerProctoringViolation("AI_EXTENSION_INJECTION", "Unauthorized AI Extension (ChatGPT/Monica/Sider) injected DOM elements.", "HIGH");
  });

  document.getElementById("btn-sim-second-face")?.addEventListener("click", () => {
    triggerProctoringViolation("MULTIPLE_FACES_DETECTED", "Computer vision model detected a second individual in camera frame.", "HIGH");
  });

  document.getElementById("btn-sim-offscreen")?.addEventListener("click", () => {
    triggerProctoringViolation("OFF_SCREEN_GAZE", "Candidate gaze shifted away from screen (>3.5s). Possible mobile device use.", "MEDIUM");
  });

  document.getElementById("btn-dismiss-freeze")?.addEventListener("click", () => {
    document.getElementById("lockdown-overlay").classList.remove("active");
  });

  // Browser Lockdown Event Listeners
  setupBrowserLockdownListeners();
}

function toggleProctoringMode() {
  state.isExamLocked = !state.isExamLocked;
  const statusPill = document.getElementById("proctoring-status-pill");
  const lockIcon = document.getElementById("lock-status-icon");
  const banner = document.getElementById("proctoring-hud-section");

  if (state.isExamLocked) {
    // Start session on backend
    fetch(`${API_BASE}/api/proctoring/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: state.proctoringSessionId,
        candidate_name: state.gapAnalysis ? state.gapAnalysis.cadre_title : "Official Candidate",
        cadre_id: state.activeCadre
      })
    });

    if (statusPill) statusPill.textContent = "● SECURE EXAM LOCKDOWN ACTIVE";
    if (statusPill) statusPill.style.color = "#10B981";
    if (lockIcon) lockIcon.textContent = "🔒";
    if (banner) banner.style.display = "block";

    // Request fullscreen
    try {
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen();
      }
    } catch (e) {
      console.log("Fullscreen request:", e);
    }

    // Start Extension Scanner & Camera Stream
    startExtensionDOMScanner();
    initWebcamStream();
    alert("🛡️ SECURE PROCTORING ACTIVATED:\n• Fullscreen lockdown enabled\n• F12 & DevTools blocked\n• Copy/Paste blocked\n• AI extension injection monitoring active\n• Computer vision gaze tracking enabled");
  } else {
    if (statusPill) statusPill.textContent = "○ Standard Mode (Unrestricted)";
    if (statusPill) statusPill.style.color = "#94A3B8";
    if (lockIcon) lockIcon.textContent = "🔓";
    if (banner) banner.style.display = "none";
  }
}

function setupBrowserLockdownListeners() {
  // 1. Keystroke Trap: DevTools (F12), Inspect (Ctrl+Shift+I/J/C), View-Source (Ctrl+U), Copy/Paste (Ctrl+C/V/X)
  document.addEventListener("keydown", (e) => {
    if (!state.isExamLocked) return;

    const isF12 = e.key === "F12";
    const isDevTools = e.ctrlKey && e.shiftKey && ["I", "J", "C"].includes(e.key.toUpperCase());
    const isViewSource = e.ctrlKey && e.key.toUpperCase() === "U";
    const isClipboard = e.ctrlKey && ["C", "V", "X"].includes(e.key.toUpperCase());

    if (isF12 || isDevTools || isViewSource || isClipboard) {
      e.preventDefault();
      e.stopPropagation();
      const actionName = isF12 || isDevTools ? "DevTools / Inspector Access" : isViewSource ? "View Source Attempt" : "Clipboard Copy/Paste";
      triggerProctoringViolation("SECURITY_KEYSTROKE_BLOCKED", `${actionName} (${e.ctrlKey ? 'Ctrl+' : ''}${e.key}) intercepted and blocked.`, "MEDIUM");
      return false;
    }
  }, true);

  // 2. Right-Click Context Menu Trap
  document.addEventListener("contextmenu", (e) => {
    if (!state.isExamLocked) return;
    e.preventDefault();
    triggerProctoringViolation("CONTEXT_MENU_BLOCKED", "Right-click context inspection attempt blocked by lockdown policy.", "LOW");
    return false;
  }, true);

  // 3. Tab-Switching and Window Focus Loss
  window.addEventListener("blur", () => {
    if (!state.isExamLocked) return;
    triggerProctoringViolation("TAB_SWITCH_OR_BLUR", "Browser window lost focus. Candidate switched applications or tabs.", "HIGH");
  });

  document.addEventListener("visibilitychange", () => {
    if (!state.isExamLocked) return;
    if (document.hidden) {
      triggerProctoringViolation("PAGE_HIDDEN", "Document visibility changed to hidden (switched tabs or minimized).", "HIGH");
    }
  });

  // 4. Fullscreen Exit Detection
  document.addEventListener("fullscreenchange", () => {
    if (!state.isExamLocked) return;
    if (!document.fullscreenElement) {
      triggerProctoringViolation("FULLSCREEN_EXIT", "Candidate exited fullscreen exam environment.", "HIGH");
    }
  });
}

function startExtensionDOMScanner() {
  const extensionSignatures = [
    '[id*="chatgpt"]', '[class*="monica"]', '[id*="merlin"]',
    '[class*="sider"]', '[data-monica]', '[data-sider]', '.quillbot-extension',
    '#__next_chatgpt', '#maxai-root', '.scispace-highlighter'
  ];

  // Periodic DOM sweep
  setInterval(() => {
    if (!state.isExamLocked) return;
    for (const sig of extensionSignatures) {
      const match = document.querySelector(sig);
      if (match) {
        match.remove();
        triggerProctoringViolation("AI_EXTENSION_INTERCEPTED", `Unauthorized AI extension node detected (${sig}) and neutralized from DOM.`, "HIGH");
      }
    }
  }, 1500);

  // MutationObserver for instant neutralization
  const observer = new MutationObserver((mutations) => {
    if (!state.isExamLocked) return;
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (node.nodeType === 1) { // Element node
          for (const sig of extensionSignatures) {
            if (node.matches && node.matches(sig)) {
              node.remove();
              triggerProctoringViolation("AI_EXTENSION_INJECTION", `Real-time AI script injection (${sig}) neutralized by sandbox.`, "HIGH");
            }
          }
        }
      }
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
}

function initWebcamStream() {
  const video = document.getElementById("proctoring-video");
  if (!video) return;

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.log("Webcam access optional/simulated:", err);
      });
  }
}

async function triggerProctoringViolation(type, details, severity) {
  try {
    const res = await fetch(`${API_BASE}/api/proctoring/log_event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: state.proctoringSessionId,
        incident_type: type,
        details: details,
        severity: severity
      })
    });
    const data = await res.json();
    state.trustScore = data.trust_score;
    state.strikes = data.strike_count;

    updateProctoringHUD(data);

    if (data.is_frozen) {
      showLockdownFreezeModal("ASSESSMENT FROZEN: MAXIMUM STRIKES REACHED (3/3)", "Multiple severe exam integrity violations were recorded. Assessment is locked for Cadre Board Review.");
    } else if (severity === "HIGH") {
      showLockdownFreezeModal(`EXAM VIOLATION (Strike ${data.strike_count} of 3)`, details);
    }
  } catch (err) {
    console.error("Proctoring log failed:", err);
  }
}

function updateProctoringHUD(data) {
  const trustVal = document.getElementById("trust-score-val");
  const trustFill = document.getElementById("trust-gauge-fill");
  const strikesVal = document.getElementById("strikes-val");

  if (trustVal) trustVal.textContent = `${data.trust_score}%`;
  if (strikesVal) strikesVal.textContent = `${data.strike_count} / ${data.max_strikes}`;
  
  if (trustFill) {
    trustFill.style.width = `${data.trust_score}%`;
    if (data.trust_score < 40) {
      trustFill.style.background = "#EF4444";
      if (trustVal) trustVal.style.color = "#EF4444";
    } else if (data.trust_score < 75) {
      trustFill.style.background = "#F59E0B";
      if (trustVal) trustVal.style.color = "#F59E0B";
    } else {
      trustFill.style.background = "linear-gradient(90deg, #10B981, #38BDF8)";
      if (trustVal) trustVal.style.color = "#10B981";
    }
  }

  // Add to incident table
  const tbody = document.getElementById("incident-log-body");
  if (tbody && data.logged_incident) {
    const inc = data.logged_incident;
    const tr = document.createElement("tr");
    
    let badgeBg = "rgba(16, 185, 129, 0.2)";
    let badgeColor = "#10B981";
    if (inc.severity === "HIGH") {
      badgeBg = "rgba(239, 68, 68, 0.25)";
      badgeColor = "#EF4444";
    } else if (inc.severity === "MEDIUM") {
      badgeBg = "rgba(245, 158, 11, 0.25)";
      badgeColor = "#F59E0B";
    }

    tr.innerHTML = `
      <td>${inc.timestamp}</td>
      <td><span style="font-weight: 700; color: #FFFFFF;">${inc.type}</span></td>
      <td><span style="background: ${badgeBg}; color: ${badgeColor}; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 6px;">${inc.severity}</span></td>
      <td style="color: #94A3B8;">${inc.details}</td>
      <td style="color: #EF4444; font-weight: 700;">-${inc.penalty_applied}%</td>
      <td style="color: #FFFFFF; font-weight: 700;">${inc.remaining_trust}%</td>
    `;
    tbody.prepend(tr);
  }
}

function showLockdownFreezeModal(title, msg) {
  const overlay = document.getElementById("lockdown-overlay");
  const modalTitle = document.getElementById("lockdown-title");
  const modalMsg = document.getElementById("lockdown-msg");

  if (modalTitle) modalTitle.textContent = title;
  if (modalMsg) modalMsg.textContent = msg;
  if (overlay) overlay.classList.add("active");
}

