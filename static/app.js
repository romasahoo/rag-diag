/* ╔═══════════════════════════════════════════╗
   ║  RAG-Diag — Frontend (FastAPI Edition)    ║
   ╚═══════════════════════════════════════════╝ */

// ─── DOM REFERENCES ─── //

const hardwareSelect  = document.getElementById('hardware-select');
const errorInput      = document.getElementById('error-input');
const runBtn          = document.getElementById('run-btn');
const inputPanel      = document.getElementById('input-panel');
const loadingPanel    = document.getElementById('loading-panel');
const loadingText     = document.getElementById('loading-text');
const progressFill    = document.getElementById('progress-fill');
const outputDashboard = document.getElementById('output-dashboard');
const errorBanner     = document.getElementById('error-banner');
const errorBannerText = document.getElementById('error-banner-text');
const statusDot       = document.getElementById('status-dot');
const statusText      = document.getElementById('status-text');
const resultSystem    = document.getElementById('result-system');
const resultCode      = document.getElementById('result-code');
const confidenceValue = document.getElementById('confidence-value');
const confidenceBadge = document.getElementById('confidence-badge');
const issueText       = document.getElementById('issue-text');
const resolutionSteps = document.getElementById('resolution-steps');
const warningText     = document.getElementById('warning-text');
const contextSource1  = document.getElementById('context-source-1');
const contextSource2  = document.getElementById('context-source-2');
const accordionBtn    = document.getElementById('accordion-trigger');
const accordionBody   = document.getElementById('accordion-content');
const resetBtn        = document.getElementById('reset-btn');

// ─── ACCORDION TOGGLE ─── //

accordionBtn.addEventListener('click', () => {
  const expanded = accordionBtn.getAttribute('aria-expanded') === 'true';
  accordionBtn.setAttribute('aria-expanded', !expanded);
  accordionBody.hidden = expanded;
});

// ─── RESET ─── //

resetBtn.addEventListener('click', () => {
  outputDashboard.hidden = true;
  errorBanner.hidden = true;
  inputPanel.style.display = '';
  statusDot.classList.remove('processing');
  statusText.textContent = 'System Ready';
  accordionBtn.setAttribute('aria-expanded', 'false');
  accordionBody.hidden = true;
  hardwareSelect.value = '';
  errorInput.value = '';
  runBtn.disabled = false;
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ─── RUN DIAGNOSTIC ─── //

runBtn.addEventListener('click', () => {
  const systemKey = hardwareSelect.value;
  const codeRaw   = errorInput.value.trim();

  // Validation
  if (!systemKey || !codeRaw) {
    if (!systemKey) hardwareSelect.parentElement.parentElement.classList.add('shake');
    if (!codeRaw) errorInput.parentElement.classList.add('shake');
    setTimeout(() => {
      document.querySelectorAll('.shake').forEach(el => el.classList.remove('shake'));
    }, 500);
    return;
  }

  runBtn.disabled = true;
  errorBanner.hidden = true;
  runDiagnosticSequence(systemKey, codeRaw);
});

// Enter key support
errorInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') runBtn.click();
});

// ─── MAIN SEQUENCE ─── //

async function runDiagnosticSequence(systemKey, codeRaw) {
  // ── Show loading ── //
  inputPanel.style.display = 'none';
  outputDashboard.hidden = true;
  loadingPanel.hidden = false;
  statusDot.classList.add('processing');
  statusText.textContent = 'Processing';

  const phases = [
    'Initializing RAG pipeline…',
    'Retrieving technical documents…',
    'Extracting relevant context chunks…',
    'Running diagnostic inference…',
    'Compiling resolution report…'
  ];

  // Start the API call in the background while showing loading phases
  const apiPromise = fetch('/api/diagnose', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ system: systemKey, error_code: codeRaw }),
  });

  // Animate through phases (minimum visual time)
  for (let i = 0; i < phases.length; i++) {
    loadingText.textContent = phases[i];
    progressFill.style.width = `${((i + 1) / phases.length) * 100}%`;
    await sleep(450 + Math.random() * 350);
  }

  // Wait for the API response (likely already resolved by now)
  let data;
  try {
    const response = await apiPromise;
    if (!response.ok) {
      const errBody = await response.json().catch(() => ({}));
      throw new Error(errBody.error || `Server error (${response.status})`);
    }
    data = await response.json();
  } catch (err) {
    // Show error state
    loadingPanel.hidden = true;
    progressFill.style.width = '0%';
    inputPanel.style.display = '';
    statusDot.classList.remove('processing');
    statusText.textContent = 'Error';
    runBtn.disabled = false;
    errorBannerText.textContent = err.message || 'An unexpected error occurred.';
    errorBanner.hidden = false;
    return;
  }

  await sleep(200);
  loadingPanel.hidden = true;
  progressFill.style.width = '0%';

  // ── Populate dashboard ── //
  resultSystem.textContent = data.system_name;
  resultCode.textContent = data.error_code;
  confidenceValue.textContent = data.confidence + '%';

  // Colour the badge based on confidence
  if (data.confidence >= 90) {
    confidenceBadge.style.background = 'rgba(34,197,94,0.12)';
    confidenceBadge.style.color = '#22c55e';
    confidenceBadge.style.borderColor = 'rgba(34,197,94,0.25)';
  } else if (data.confidence >= 80) {
    confidenceBadge.style.background = 'rgba(245,158,11,0.12)';
    confidenceBadge.style.color = '#f59e0b';
    confidenceBadge.style.borderColor = 'rgba(245,158,11,0.25)';
  } else {
    confidenceBadge.style.background = 'rgba(239,68,68,0.12)';
    confidenceBadge.style.color = '#ef4444';
    confidenceBadge.style.borderColor = 'rgba(239,68,68,0.25)';
  }

  issueText.textContent = data.issue;

  // Build steps
  resolutionSteps.innerHTML = '';
  data.steps.forEach(step => {
    const li = document.createElement('li');
    li.innerHTML = `
      <div class="step-content">
        <div class="step-title">${escapeHtml(step.title)}</div>
        <div class="step-detail">${escapeHtml(step.detail)}</div>
      </div>`;
    resolutionSteps.appendChild(li);
  });

  warningText.textContent = data.warning;

  // Raw context sources
  contextSource1.setAttribute('data-source', data.sources[0].label);
  contextSource1.textContent = data.sources[0].text;
  contextSource2.setAttribute('data-source', data.sources[1].label);
  contextSource2.textContent = data.sources[1].text;

  // Reset accordion
  accordionBtn.setAttribute('aria-expanded', 'false');
  accordionBody.hidden = true;

  // Show dashboard
  statusDot.classList.remove('processing');
  statusText.textContent = 'Diagnostic Complete';
  outputDashboard.hidden = false;
  outputDashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ─── UTILITIES ─── //

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
