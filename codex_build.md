# AI TRIAGE SYSTEM - CODEX BUILD SCRIPT v2 (Extended Edition)

## Project: `triage_ai v2`

### Objective

This project aims to advance the original KTAS-based automated triage system by integrating a fully interactive NLP assistant via TalkBot, Django REST APIs for backend communication, and a scalable ML pipeline. The solution will dynamically request missing fields from the patient using natural language prompts, convert human descriptions to standardized scales, and deliver predictions in real time. The project will also feature audit logging, override logic for clinical review, and a user-facing frontend to enable direct usage by non-technical staff.

---

## Directory Structure (Detailed)

```
# Project root directory
triage_ai/
├─ manage.py                        # Main Django entry point
├─ requirements.txt                 # Package dependencies for the project
├─ Dockerfile                       # Image definition for deployment
├─ docker-compose.yml              # Multi-container setup configuration

# Data and literature
├─ data/
│   └─ triage_data.csv              # Primary dataset used for ML training
├─ docs/
│   └─ triage.pdf                   # Core research paper used as reference

# Frontend application for triage interaction
├─ front/
│   ├─ index.html                   # Web interface for user data entry
│   ├─ styles.css                   # CSS for styling components
│   └─ scripts.js                   # JS handling user interaction and AJAX

# Main Django settings and URL router
├─ triage_ai/
│   ├─ __init__.py, settings.py     # Config and environment setup
│   └─ urls.py                      # Global route definitions

# Primary ML and business logic app
└─ triage_ml/
    ├─ ml_pipeline/                 # ML preprocessing and model ops
    │   ├─ preprocess.py            # Cleans, scales, and encodes input
    │   ├─ train_model.py           # Model training and evaluation
    │   └─ artifacts/               # Stores models and label encoders
    ├─ utils.py                     # Helper functions (e.g., metrics)
    ├─ models.py                    # Django DB models including CaseLog
    ├─ serializers.py               # Request/response validators
    ├─ views.py                     # Logic for each endpoint
    ├─ urls.py                      # API routes
    ├─ admin.py                     # Admin panel registration
    ├─ output.py                    # Converts raw predictions to messages
    ├─ change_scale.py              # Bidirectional mapping for pain scoring
    ├─ tests/                       # Unit + integration tests
    ├─ migrations/                  # Database versioning
    └─ tasks/                       # Task handlers and TalkBot agents
        ├─ response_engine.py       # NLP controller for async prompts
        ├─ input.py                 # Message construction from missing fields
        ├─ cleaner.py               # Parses and standardizes AI responses
        └─ generate_response.py     # Formats AI output for user delivery
```

---

## Machine Learning Training Pipeline (`train_model.py`)

1. Load dataset from `triage_data.csv`
2. Preprocessing:
   - Normalize vital signs
   - Bucket NRS pain into ordinal values
   - Create binary central pain indicator
   - Impute or drop missing values
3. Train `RandomForestClassifier` with `GridSearchCV`
4. Evaluate:
   - Accuracy
   - Cohen’s Kappa
   - Pearson correlation coefficient
   - Confusion Matrix
5. Serialize model using `joblib` to `artifacts/model.pkl`

---

## Required Dependencies (`requirements.txt`)

```
Django==5.0
scikit-learn==1.5
pandas==2.2
numpy
joblib
requests
djangorestframework==3.15
drf-yasg==2.2.0
scipy
```

---

## REST API Endpoint (`/api/triage/predict/`)

### Example Request:

```json
{
  "pid": "12345",
  "Age": 67,
  "Sex": "Female",
  "SBP": 145,
  "DBP": 95,
  "HR": 82,
  "RR": 20,
  "BT": 38.0,
  "SpO2": 94,
  "NRS_pain": 7,
  "Pain_axis": "central",
  "Chief_complain": "abdominal cramps",
  "Arrival_mode": "walk-in",
  "KTAS_expert": 3
}
```

### Example Response:

```json
{
  "message": "Patient likely falls under KTAS level 3. Immediate nurse review is recommended."
}
```

### Clinical Override Rule:

```
If predicted KTAS >= 4 AND NRS_pain >= 7 AND Pain_axis == "central",
then override prediction to 3 and flag as NEED-RN-REVIEW
```

---

## Case Logging (`CaseLog` model)

For every POST request:

- Patient ID (optional)
- Complete payload stored in JSONField
- Predicted KTAS level
- Expert label (if provided)
- Flagged condition if override was triggered
- Timestamps for audit

---

## TalkBot Integration Workflow

The `response_engine.py` drives communication with the LLM:

- Uses `input.py` to detect missing patient fields
- Constructs user-friendly prompts dynamically
- Sends queries via `requests.post` to TalkBot API
- Parses JSON result using `cleaner.py`
- Sends structured fields to `generate_response.py`

### TalkBot API Endpoint:

```
POST https://api.talkbot.ir/v1/chat/completions
```

### Sample Prompt:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "You are an ER triage nurse assistant."},
    {"role": "user", "content": "Patient reports blurry vision and nausea."}
  ]
}
```

### Expected Completion:

```json
{
  "message": "On a scale from 0 (no pain) to 10 (worst imaginable), how intense is the pain?",
  "context": {
    "missing_fields": ["NRS_pain", "Pain_axis"]
  }
}
```

---

## Pain Score Normalization Logic (`change_scale.py`)

- Converts common phrases (e.g., "throbbing", "agonizing") into NRS equivalents
- Bidirectional translation:
  - User input → model format
  - Model feedback → human readable
- Maintains consistency in prediction logic

---

## Frontend UI (`front/`)

- `index.html`: Responsive form with step-wise field collection
- `styles.css`: Theme styling with severity awareness (color-coded feedback)
- `scripts.js`: Interactive logic for auto-progression + field checking
- Fetch API used for POST/GET

---

## Testing Suite

- Unit tests for `change_scale`, `preprocess`, `utils`
- Integration tests for `/api/triage/predict/`
- Frontend tests (JS validation)
- NLP flow simulated using mock TalkBot calls

---

## Deployment Workflow

- Use official `python:3.12-slim` Docker image
- Add PostgreSQL or fallback SQLite container
- Load fixtures for demo mode
- Expose API docs via `drf-yasg` Swagger UI at `/swagger/`

---

## Final DevOps Checklist

- Python code linted via `black` + `flake8`
- Sensitive keys hidden in `.env`
- Logging of inference errors
- TalkBot error handling retries
- Offline mode available (if no NLP required)

---

### Note:

Ensure infrastructure supports horizontal scaling, NLP caching, and encrypted logging for compliance in real-world deployment.

