import os
import json
import datetime as dt
from flask import Flask, request, render_template_string, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "dev-secret")

INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Anonymous Self-Triage</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <h1 class="mb-4 text-primary">Anonymous Self-Triage</h1>
  <p class="lead">Get generalized guidance based on your symptoms and vital signs.
  <strong>This tool does NOT provide medical advice or diagnosis.</strong></p>

  <form action="{{ url_for('submit') }}" method="post" class="card p-4 shadow-sm">
    <h4 class="mb-3">About you</h4>
    <div class="mb-3">
      <label class="form-label">Age (years)</label>
      <input type="number" class="form-control" name="age" min="0" max="120" required>
    </div>
    <div class="mb-3">
      <label class="form-label">Sex</label>
      <select class="form-select" name="sex" required>
        <option value="" disabled selected>-- Select --</option>
        <option value="F">Female</option>
        <option value="M">Male</option>
        <option value="X">Prefer not to say / Other</option>
      </select>
    </div>

    <h4 class="mt-4 mb-3">Your symptoms</h4>
    <div class="mb-3">
      <label class="form-label">Symptom description</label>
      <textarea class="form-control" name="symptoms" rows="4" required></textarea>
    </div>
    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Duration (days)</label>
        <input type="number" class="form-control" name="duration_days" min="0" required>
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Pain (0-10)</label>
        <input type="number" class="form-control" name="pain_score" min="0" max="10" required>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Fever (°F)</label>
        <input type="number" class="form-control" name="fever_f" min="90" max="110" step="0.1">
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Blood Pressure</label>
        <div class="input-group">
          <input type="number" class="form-control" name="bp_sys" placeholder="Systolic">
          <span class="input-group-text">/</span>
          <input type="number" class="form-control" name="bp_dia" placeholder="Diastolic">
        </div>
      </div>
    </div>
    <div class="mb-3">
      <label class="form-label">Pulse / Heart Rate</label>
      <input type="number" class="form-control" name="pulse" min="30" max="200">
    </div>

    <button type="submit" class="btn btn-primary btn-lg w-100 py-3">Get guidance</button>
  </form>
</div>
</body>
</html>
"""

GUIDANCE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Guided Result</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <h1 class="text-success mb-4">Generalized Guidance (Simulated AI)</h1>
  <div class="card p-4 shadow-sm">
    <h4>Severity: {{ result['severity'] }}</h4>
    <p><strong>Guidance:</strong> {{ result['guidance'] }}</p>
    <p><em>Reason:</em> {{ result['reason'] }}</p>
  </div>
  <p class="mt-4"><a href="{{ url_for('index') }}" class="btn btn-outline-primary btn-lg">Back to Start</a></p>
</div>
</body>
</html>
"""

def simulate_ai_scoring(payload):
    age = payload.get("age")
    pain = payload.get("pain_score", 0)
    fever_f = payload.get("fever_f")
    duration = payload.get("duration_days", 0)
    bp_sys = payload.get("bp_sys")
    bp_dia = payload.get("bp_dia")
    pulse = payload.get("pulse")
    text = (payload.get("symptoms") or "").lower()

    severe_terms = any(t in text for t in [
        "chest pain", "shortness of breath", "stroke", "fainting", "severe bleeding",
        "confusion", "unconscious"
    ])

    high_fever = (fever_f is not None and fever_f >= 103)
    moderate_fever = (fever_f is not None and 100 <= fever_f < 103)
    risk_age = (age is not None and (age < 5 or age >= 65))

    abnormal_bp = (bp_sys is not None and bp_sys >= 180) or (bp_dia is not None and bp_dia >= 120)
    low_bp = (bp_sys is not None and bp_sys < 90) or (bp_dia is not None and bp_dia < 60)
    tachycardia = (pulse is not None and pulse > 120)
    bradycardia = (pulse is not None and pulse < 50)

    if severe_terms or pain >= 8 or high_fever or abnormal_bp or tachycardia or bradycardia or (risk_age and moderate_fever):
        return {"severity": "Severe", "guidance": "Consider urgent evaluation.", "reason": "Red-flag symptoms, abnormal vitals, or high pain/fever"}
    if pain >= 5 or moderate_fever or duration >= 3 or low_bp:
        return {"severity": "Moderate", "guidance": "Consider timely clinical follow-up.", "reason": "Moderate pain/fever, prolonged symptoms, or low blood pressure"}
    return {"severity": "Mild", "guidance": "Self-care may be reasonable; monitor for changes.", "reason": "Vitals within typical ranges, low pain, short duration"}

@app.route("/", methods=["GET"])
def index():
    # First load: form only, no history, no extra buttons
    return render_template_string(INDEX_HTML)

@app.route("/submit", methods=["POST"])
def submit():
    # Immediately compute and show guidance after one click (no intermediate button)
    try:
        age = int(request.form.get("age"))
        sex = request.form.get("sex")
        symptoms = request.form.get("symptoms")
        duration_days = int(request.form.get("duration_days", "0"))
        pain_score = int(request.form.get("pain_score", "0"))

        fever_f = float(request.form.get("fever_f")) if request.form.get("fever_f") else None
        bp_sys = int(request.form.get("bp_sys")) if request.form.get("bp_sys") else None
        bp_dia = int(request.form.get("bp_dia")) if request.form.get("bp_dia") else None
        pulse = int(request.form.get("pulse")) if request.form.get("pulse") else None

        payload = {
            "age": age,
            "sex": sex,
            "symptoms": symptoms,
            "duration_days": duration_days,
            "pain_score": pain_score,
            "fever_f": fever_f,
            "bp_sys": bp_sys,
            "bp_dia": bp_dia,
            "pulse": pulse,
            "timestamp_utc": dt.datetime.utcnow().isoformat(timespec="seconds")
        }

        result = simulate_ai_scoring(payload)
        return render_template_string(GUIDANCE_HTML, result=result)

    except Exception as e:
        flash(f"Submission failed: {e}")
        return redirect(url_for("index"))

if __name__ == "__main__":
    # Local default port; Azure uses PORT env
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(debug=True, host=host, port=port)