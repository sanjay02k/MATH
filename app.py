from flask import Flask, render_template_string, request, jsonify
import math

app = Flask(__name__)

def calculate_risk(glucose, bmi, age, family):
    def factor(value, threshold, scale):
        return 1 / (1 + math.exp((threshold - value) / scale))

    return 100 * (
        0.40 * factor(glucose, 126, 18)
        + 0.25 * factor(bmi, 25, 4)
        + 0.20 * factor(age, 45, 12)
        + 0.15 * (family == "Yes")
    )

PAGE = r'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Diabetes Risk Prediction</title>
<style>
:root{--red:#e50920;--yellow:#ffd600;--black:#050505;--panel:#101010;--panel2:#181818;--white:#fff;--muted:#aaa}
*{box-sizing:border-box}body{margin:0;background:var(--black);color:var(--white);font-family:Segoe UI,Arial,sans-serif;min-height:100vh}
header{height:58px;background:var(--red);display:flex;align-items:center;padding:0 28px;font-size:18px;font-weight:700}
main{max-width:1250px;margin:auto;padding:18px 28px 12px}.title{font-size:38px;font-weight:800;margin:6px 0 4px}.title span{color:var(--red)}.subtitle{font-size:12px;letter-spacing:3px;margin-bottom:18px;color:var(--muted)}
.grid{display:grid;grid-template-columns:1.04fr .96fr;gap:12px}.card{background:var(--panel);border:1px solid var(--red);min-height:440px}.card.result{border-color:#5a4d16}
.cardhead{height:58px;background:var(--red);display:flex;align-items:center;justify-content:space-between;padding:0 18px}.cardhead strong{font-size:17px}.cardhead small{color:white}.resulthead{height:58px;background:var(--yellow);color:#9e0011;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:17px;font-weight:800}
form{padding:14px 20px}.field{display:grid;grid-template-columns:145px 1fr;align-items:center;margin-bottom:8px;min-height:58px}.field label{font-weight:700}.field small{display:block;color:var(--muted);font-weight:400;margin-top:3px}.field input,.field select{width:100%;height:44px;background:#050505;color:white;border:1px solid #a68e25;border-radius:6px;padding:0 14px;font-size:16px;outline:none}.field input:focus,.field select:focus{border-color:var(--yellow)}
button{display:block;width:78%;height:52px;border:0;border-radius:11px;color:white;background:var(--red);font-size:15px;font-weight:800;cursor:pointer;margin:14px auto 0}.clear{height:38px;background:transparent;color:var(--muted);margin-top:2px}
.resultbody{min-height:380px;padding:14px 18px;display:grid;grid-template-rows:1fr auto;gap:10px}.result-top{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:14px;min-height:250px}.gauge-wrap{display:flex;align-items:center;justify-content:center}.gauge{width:min(210px,100%);aspect-ratio:1;border-radius:50%;position:relative;background:conic-gradient(var(--risk) var(--percent),#333 0);display:grid;place-items:center;transition:.35s}
.gauge:before{content:"";position:absolute;width:78%;height:78%;border-radius:50%;background:var(--panel)}.gauge-inner{position:relative;text-align:center}.gauge-inner .value{font-size:clamp(34px,4vw,48px);font-weight:900;color:var(--risk)}.gauge-inner .label{font-size:12px;color:var(--white);font-weight:bold}.status-panel{border:1px solid #8b7621;border-radius:8px;background:#17140b;padding:15px 12px}.status-title{font-size:13px;font-weight:700;margin-bottom:12px}.status{text-align:center}.status strong{font-size:20px}.description{min-height:44px;text-align:center;color:var(--muted);font-size:12px;padding:8px 2px}.risk-meter{display:flex;align-items:center;gap:10px;font-weight:700}.meter-track{height:18px;flex:1;background:#393939;border-radius:12px;overflow:hidden}.meter-fill{height:100%;width:0;background:var(--yellow);border-radius:12px;transition:width .35s,background .35s}.meter-value{min-width:48px;text-align:right}.error{color:#ff8b8b;text-align:center;min-height:20px;margin-top:5px}
@media(max-width:850px){.grid{grid-template-columns:1fr}.card{min-height:auto}.field{grid-template-columns:130px 1fr}.result-top{min-height:220px}.gauge{width:min(210px,100%)}.title{font-size:30px}}
@media(max-width:480px){header{padding:0 16px;font-size:15px}main{padding:16px}.cardhead{padding:0 12px}.cardhead small{font-size:11px}.resultbody{padding:12px}.result-top{grid-template-columns:1fr 1fr;gap:8px}.status-panel{padding:12px 8px}.status strong{font-size:16px}.field{grid-template-columns:115px 1fr}.field label{font-size:14px}}
</style></head><body>
<header>♥ &nbsp; Diabetes Risk Prediction Using Bayes</header>
<main><div class="title">Diabetes <span>Risk Prediction</span></div><div class="subtitle">USING BAYESIAN APPROACH</div>
<div class="grid"><section class="card"><div class="cardhead"><strong>♟ &nbsp; Patient Information</strong><small>Enter your details below</small></div>
<form id="form"><div class="field"><label>Glucose Level<small>(mg/dL)</small></label><input id="glucose" type="number" min="20" max="600" value="150" required></div><div class="field"><label>BMI<small>(kg/m²)</small></label><input id="bmi" type="number" min="10" max="100" step="0.1" value="29" required></div><div class="field"><label>Age<small>(years)</small></label><input id="age" type="number" min="1" max="120" value="50" required></div><div class="field"><label>Family History<small>(of Diabetes)</small></label><select id="family"><option>No</option><option>Yes</option></select></div><button type="submit">⌕ &nbsp; PREDICT RISK</button><button type="button" class="clear" onclick="clearForm()">CLEAR INPUTS</button><div id="error" class="error"></div></form></section>
<section class="card result"><div class="resulthead">▥ &nbsp; Prediction Result</div><div class="resultbody"><div class="result-top"><div class="gauge-wrap"><div class="gauge" id="gauge" style="--percent:0%;--risk:#ffd600"><div class="gauge-inner"><div class="value" id="value">--%</div><div class="label">RISK SCORE</div></div></div></div><div class="status-panel"><div class="status"><strong id="status" style="color:#00e676">♥ Awaiting Input</strong></div><div class="description" id="description">Enter patient details and click Predict Risk.</div></div></div><div class="risk-meter"><div class="meter-track"><div class="meter-fill" id="meter"></div></div><span class="meter-value" id="meter-value">--%</span></div></div></section></div></main>
<script>
function clearForm(){document.getElementById('glucose').value='150';document.getElementById('bmi').value='29';document.getElementById('age').value='50';document.getElementById('family').value='No';document.getElementById('value').textContent='--%';document.getElementById('gauge').style.setProperty('--percent','0%');document.getElementById('gauge').style.setProperty('--risk','#ffd600');document.getElementById('status').textContent='♥ Awaiting Input';document.getElementById('status').style.color='#00e676';document.getElementById('description').textContent='Enter patient details and click Predict Risk.';document.getElementById('meter').style.width='0%';document.getElementById('meter-value').textContent='--%';document.getElementById('error').textContent=''}
document.getElementById('form').onsubmit=async e=>{e.preventDefault();const body={glucose:+document.getElementById('glucose').value,bmi:+document.getElementById('bmi').value,age:+document.getElementById('age').value,family:document.getElementById('family').value};const r=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const d=await r.json();if(!r.ok){document.getElementById('error').textContent=d.error;return}document.getElementById('error').textContent='';const gauge=document.getElementById('gauge');gauge.style.setProperty('--percent',d.risk+'%');gauge.style.setProperty('--risk',d.color);document.getElementById('value').textContent=d.risk.toFixed(1)+'%';document.getElementById('value').style.color=d.color;document.getElementById('status').textContent=d.status;document.getElementById('status').style.color=d.color;document.getElementById('description').textContent=d.description;document.getElementById('meter').style.width=d.risk+'%';document.getElementById('meter').style.background=d.color;document.getElementById('meter-value').textContent=d.risk.toFixed(1)+'%'};
</script></body></html>'''

@app.get('/')
def index(): return render_template_string(PAGE)

@app.post('/predict')
def predict():
    try:
        body=request.get_json()
        glucose=float(body['glucose']); bmi=float(body['bmi']); age=int(body['age']); family=body['family']
        if not (20 <= glucose <= 600 and 10 <= bmi <= 100 and 1 <= age <= 120) or family not in ('No', 'Yes'): return jsonify(error='Enter valid glucose, BMI, age, and family history values.'),400
        risk=calculate_risk(glucose,bmi,age,family)
        if risk>=80: color='#e50920'; status='▲  High Risk'; description='Your risk is high. Please consult a qualified healthcare professional promptly.'
        elif risk>=50: color='#ffd600'; status='●  Moderate Risk'; description='Your risk is moderate. Consider lifestyle changes and consult a healthcare professional.'
        else: color='#00e676'; status='♥  Low Risk'; description='Your risk is low. Maintain healthy habits and regular checkups.'
        return jsonify(risk=risk,color=color,status=status,description=description)
    except Exception: return jsonify(error='Enter valid positive numbers for glucose, BMI and age.'),400

if __name__=='__main__': app.run(host='0.0.0.0',port=5000,debug=False)