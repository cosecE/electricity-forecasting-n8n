# electricity-forecasting-n8n
fast API code + json file for the n8n workflow


# 🚀 How to Run

## Prerequisites

* Docker Desktop
* Python 3.8+
* pip
* (Windows) WSL recommended

---

## ⚙️ 1. Start FastAPI (Backend)

```bash
# Navigate to project folder
cd /path/to/project

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pandas

# Run API
uvicorn forecast_api:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🐳 2. Start n8n (Agentic Workflow)

```bash
docker run -it --rm \
--name n8n \
-p 5678:5678 \
-e GENERIC_TIMEZONE="America/New_York" \
-e TZ="America/New_York" \
-v "$(pwd)/.n8n:/home/node/.n8n" \
docker.n8n.io/n8nio/n8n
```

Open:

```
http://localhost:5678
```

---

## 🔗 3. Connect n8n → API

In HTTP node:

* **Method:** POST
* **URL:**

```
http://host.docker.internal:8000/forecast
```

* **Body:**

```json
{
  "entity_id": "{{ $json.output.entity_id }}"
}
```

---

## 4. Test the Workflow

Example prompt:

```
Give me forecast for MT_158
```

---

## Troubleshooting

* Use `/docs` (not root URL)
* Ensure entity exists in `cluster_assignments.csv`
* Use `host.docker.internal` (not `127.0.0.1`) inside Docker
* Wait if LLM rate limits occur

---

# Notes

* Forecasts are **cluster-based (Low / Medium / High)**
* Results come from **precomputed SARIMAX outputs**
* LLM provides **natural language interpretation**

---

