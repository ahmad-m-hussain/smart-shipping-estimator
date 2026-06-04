# ── Base Image ──────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Working Directory ────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Dependencies ─────────────────────────────────────────────────────
# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# ── Copy Application Files ───────────────────────────────────────────────────
COPY app.py .

# ── Expose Port ──────────────────────────────────────────────────────────────
EXPOSE 5000

# ── Start Application with Gunicorn ──────────────────────────────────────────
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
