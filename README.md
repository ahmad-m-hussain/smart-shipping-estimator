# 📦 Smart Shipping Cost Estimator

A containerized Flask web app for estimating shipping costs, built with Docker and automated via a Jenkins CI/CD pipeline.

---

## 🗂️ Project Structure

```
smart-shipping-estimator/
├── app.py              # Flask application (UI + logic)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build instructions
└── Jenkinsfile         # CI/CD pipeline definition
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask 3.0 |
| Production Server | Gunicorn |
| Containerization | Docker |
| CI/CD Automation | Jenkins (Declarative Pipeline) |
| Base Image | python:3.11-slim |

---

## ⚙️ How It Works

1. The user fills in **Package Weight (kg)**, **Distance (km)**, and **Shipping Mode** (Express / Standard).
2. On form submit, the Flask app processes the input and returns a success confirmation message.
3. The app is served by **Gunicorn** inside a Docker container on port `5000`.

---

## 🚀 Quick Start

### Run Locally (without Docker)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the app
python app.py

# 3. Open in browser
http://localhost:5000
```

### Run with Docker

```bash
# 1. Build the image
docker build -t shipping-app .

# 2. Run the container
docker run -d --name shipping-container -p 5000:5000 shipping-app

# 3. Open in browser
http://localhost:5000
```

### Stop & Remove Container

```bash
docker stop shipping-container
docker rm shipping-container
```

---

## 🔁 Jenkins CI/CD Pipeline

The `Jenkinsfile` defines a 3-stage declarative pipeline:

```
Checkout SCM  →  Build Docker Image  →  Deploy Container
```

| Stage | Action |
|---|---|
| **Checkout SCM** | Pulls the latest code from the configured Git repository |
| **Build Docker Image** | Builds and tags the image as `shipping-app` |
| **Deploy Container** | Stops/removes any existing container, then runs a fresh one on port `5000` |

### Jenkins Setup Steps

1. Create a **New Item** → **Pipeline** in Jenkins.
2. Under *Pipeline*, set **Definition** to `Pipeline script from SCM`.
3. Set **SCM** to `Git` and enter your repository URL.
4. Set **Script Path** to `Jenkinsfile`.
5. Click **Save** and then **Build Now**.

---

## 🐳 Docker Details

| Property | Value |
|---|---|
| Base Image | `python:3.11-slim` |
| Working Directory | `/app` |
| Exposed Port | `5000` |
| Entry Point | `gunicorn --bind 0.0.0.0:5000 --workers 2 app:app` |
| Restart Policy | `unless-stopped` |

---

## 📋 Requirements

- Python 3.11+
- Docker Engine
- Jenkins (with Docker available on the agent)

---

## 📄 License

This project is intended for educational purposes.
