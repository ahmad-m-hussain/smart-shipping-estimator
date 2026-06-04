from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Shipping Cost Estimator</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg:        #0b0f1a;
            --surface:   #111827;
            --border:    #1f2d45;
            --accent:    #2563eb;
            --accent-hi: #3b82f6;
            --success:   #10b981;
            --text:      #f1f5f9;
            --muted:     #94a3b8;
            --glow:      rgba(37,99,235,.35);
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'DM Sans', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            background-image:
                radial-gradient(ellipse 80% 50% at 50% -10%, rgba(37,99,235,.18), transparent),
                radial-gradient(ellipse 40% 30% at 80% 90%, rgba(16,185,129,.08), transparent);
        }

        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2.8rem 3rem;
            width: 100%;
            max-width: 520px;
            box-shadow: 0 0 60px rgba(0,0,0,.5), 0 0 0 1px rgba(255,255,255,.04) inset;
            animation: rise .5s cubic-bezier(.22,1,.36,1);
        }

        @keyframes rise {
            from { opacity: 0; transform: translateY(28px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .logo-row {
            display: flex;
            align-items: center;
            gap: .75rem;
            margin-bottom: 1.8rem;
        }

        .logo-icon {
            width: 44px; height: 44px;
            background: linear-gradient(135deg, var(--accent), var(--accent-hi));
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.3rem;
            box-shadow: 0 0 18px var(--glow);
            flex-shrink: 0;
        }

        h1 {
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: -.01em;
            line-height: 1.2;
        }

        h1 span { color: var(--accent-hi); }

        .subtitle {
            font-size: .78rem;
            color: var(--muted);
            font-weight: 300;
            margin-top: .15rem;
        }

        .divider {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.5rem 0;
        }

        .field { margin-bottom: 1.3rem; }

        label {
            display: block;
            font-size: .72rem;
            font-weight: 500;
            color: var(--muted);
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: .5rem;
        }

        input, select {
            width: 100%;
            background: rgba(255,255,255,.04);
            border: 1px solid var(--border);
            border-radius: 10px;
            color: var(--text);
            font-family: 'DM Sans', sans-serif;
            font-size: .95rem;
            padding: .75rem 1rem;
            outline: none;
            transition: border-color .2s, box-shadow .2s;
            appearance: none;
        }

        input:focus, select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--glow);
        }

        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 1rem center;
            cursor: pointer;
        }

        select option { background: #1e2a3a; }

        .btn {
            width: 100%;
            margin-top: .5rem;
            padding: .85rem 1rem;
            background: linear-gradient(135deg, var(--accent), var(--accent-hi));
            border: none;
            border-radius: 10px;
            color: #fff;
            font-family: 'Syne', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: .02em;
            cursor: pointer;
            transition: opacity .2s, transform .15s, box-shadow .2s;
            box-shadow: 0 4px 20px var(--glow);
        }

        .btn:hover  { opacity: .9; transform: translateY(-1px); box-shadow: 0 6px 28px var(--glow); }
        .btn:active { transform: translateY(0); opacity: 1; }

        /* ── Result banner ── */
        .result {
            margin-top: 1.6rem;
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            display: flex;
            align-items: flex-start;
            gap: .85rem;
            background: rgba(16,185,129,.08);
            border: 1px solid rgba(16,185,129,.3);
            animation: popIn .4s cubic-bezier(.22,1,.36,1);
        }

        @keyframes popIn {
            from { opacity: 0; transform: scale(.97); }
            to   { opacity: 1; transform: scale(1); }
        }

        .result-icon {
            font-size: 1.4rem;
            line-height: 1;
            flex-shrink: 0;
            margin-top: .05rem;
        }

        .result-text {
            font-size: .92rem;
            color: #6ee7b7;
            font-weight: 500;
            line-height: 1.5;
        }

        .result-meta {
            margin-top: .55rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .tag {
            background: rgba(16,185,129,.12);
            border: 1px solid rgba(16,185,129,.2);
            border-radius: 6px;
            padding: .25rem .65rem;
            font-size: .72rem;
            color: #a7f3d0;
            letter-spacing: .04em;
            text-transform: uppercase;
        }

        .footer-note {
            text-align: center;
            font-size: .7rem;
            color: rgba(148,163,184,.4);
            margin-top: 2rem;
            letter-spacing: .05em;
        }
    </style>
</head>
<body>
<div class="card">

    <div class="logo-row">
        <div class="logo-icon">📦</div>
        <div>
            <h1>Smart <span>Shipping</span> Estimator</h1>
            <p class="subtitle">Containerised · Powered by Flask</p>
        </div>
    </div>

    <hr class="divider">

    <form method="POST" action="/">

        <div class="field">
            <label>Package Weight (kg)</label>
            <input
                type="number"
                name="weight"
                placeholder="e.g. 2.5"
                step="0.1" min="0.1"
                value="{{ weight or '' }}"
                required
            >
        </div>

        <div class="field">
            <label>Distance (km)</label>
            <input
                type="number"
                name="distance"
                placeholder="e.g. 350"
                step="1" min="1"
                value="{{ distance or '' }}"
                required
            >
        </div>

        <div class="field">
            <label>Shipping Mode</label>
            <select name="mode" required>
                <option value="" disabled {% if not mode %}selected{% endif %}>Select a mode…</option>
                <option value="Express"  {% if mode == 'Express'  %}selected{% endif %}>🚀 Express</option>
                <option value="Standard" {% if mode == 'Standard' %}selected{% endif %}>🚢 Standard</option>
            </select>
        </div>

        <button type="submit" class="btn">Calculate Shipping</button>
    </form>

    {% if result %}
    <div class="result">
        <div class="result-icon">✅</div>
        <div>
            <div class="result-text">{{ result }}</div>
            <div class="result-meta">
                <span class="tag">{{ mode }}</span>
                <span class="tag">{{ weight }} kg</span>
                <span class="tag">{{ distance }} km</span>
            </div>
        </div>
    </div>
    {% endif %}

    <p class="footer-note">DOCKER READY · PORT 5000 · 0.0.0.0</p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result   = None
    weight   = None
    distance = None
    mode     = None

    if request.method == "POST":
        weight   = request.form.get("weight")
        distance = request.form.get("distance")
        mode     = request.form.get("mode")

        result = "Success! Your shipping request has been processed. Container is running perfectly!"

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        weight=weight,
        distance=distance,
        mode=mode,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
