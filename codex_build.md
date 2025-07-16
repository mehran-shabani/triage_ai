# === CODEX BUILD SCRIPT ===
# Project: triage_ai
# Goal: Build a robust AI-powered KTAS triage system
# Inputs provided:
#   • data/triage_data.csv.csv   ← tabular training data
#   • docs/triage.pdf           ← clinical/scientific reference

############################################################
## SECTION A · Repository skeleton
############################################################
1. Create this directory tree:

   triage_ai/
   ├─ manage.py
   ├─ requirements.txt
   ├─ Dockerfile
   ├─ docker-compose.yml
   ├─ data/triage_data.csv.csv
   ├─ docs/triage.pdf
   ├─ triage_ai/          ← Django project settings
   └─ triage_ml/          ← Django app & ML logic
       ├─ ml_pipeline/
       │   ├─ preprocess.py
       │   ├─ train_model.py
       │   └─ artifacts/
       ├─ utils.py
       ├─ models.py
       ├─ serializers.py
       ├─ views.py
       ├─ urls.py
       ├─ admin.py
       ├─ tests/
       └─ migrations/

############################################################
## SECTION B · Python dependencies
############################################################
2. Populate **requirements.txt**:

   Django==5.0
   djangorestframework==3.15
   drf-yasg==2.2.0
   scikit-learn==1.5
   pandas==2.2
   numpy
   joblib
   scipy

############################################################
## SECTION C · ML training pipeline
############################################################
3. In **triage_ml/ml_pipeline/train_model.py**:

   a) Load data/triage_data.csv.csv
   b) Use preprocess.py to:
      • Convert NRS_pain → Pain_severity (mild/moderate/severe)
      • Add pain_central_severe (boolean: pain severe & central)
   c) Use StandardScaler for numeric, OneHotEncoder for categoric
   d) Model: RandomForestClassifier (n_estimators=300, class_weight='balanced_subsample')
   e) Evaluate on holdout test (20%, stratified by KTAS_expert):
      • Print accuracy, weighted κ (quadratic), Pearson r
   f) Save the fitted pipeline as artifacts/model.pkl

############################################################
## SECTION D · API contract
############################################################
4. Expose one endpoint via DRF:

   POST /api/triage/predict/
   ------------------------------------
   Request (JSON):
     {
       "pid": "optional string",
       "Age": 71,
       "Sex": "Male|Female",
       "SBP": 160,
       "DBP": 100,
       "HR": 84,
       "RR": 18,
       "BT": 37.4,
       "SpO2": 98,
       "NRS_pain": 8,
       "Pain_axis": "central|peripheral",
       "Chief_complain": "free text ≤120 chars",
       "Arrival_mode": "string",
       "KTAS_expert": 3      # optional ground-truth label
     }

   Response (JSON):
     {
       "ktas_predicted": 3,
       "flag": "NEED-RN-REVIEW" | null
     }

   Business rule (pain guard):
     • If model predicts ≥4 AND NRS_pain ≥ 7 AND Pain_axis=="central"
       → override prediction to 3, set flag to "NEED-RN-REVIEW".

############################################################
## SECTION E · Data logging for future retraining
############################################################
5. For every API call (every patient/case), **store**:

   - pid (if present)
   - all model input fields
   - model's predicted KTAS
   - KTAS_expert (if present)
   - is_error (True if KTAS_expert present and prediction ≠ label)
   - created_at (timestamp)

   Implement as Django model: `CaseLog`.
   All records are saved in the project database.
   These records **must be queryable/exportable for future manual retraining or performance audits**.

   No automated retraining is required at this stage: just accumulate and store all data for potential future use.

############################################################
## SECTION F · Metrics
############################################################
6. In utils.py, provide:

   - compute_kappa(y_true, y_pred)
   - compute_pearson(y_true, y_pred)

   (So metrics can be computed later from CaseLog records.)

############################################################
## SECTION G · Documentation & Dev UX
############################################################
7. Provide `/swagger/` docs via drf-yasg.
8. Provide Dockerfile and docker-compose.yml (web + DB).
9. README.md with usage, endpoint documentation, and citation to docs/triage.pdf
10. Create a documantion for how to use this app for best efficacy and how dev this for future
11.Generate docs/flutter_roadmap.txt for how to use API and instruction of this app for flutter apps
12. create a task that make this project better and rise efficaxy of that with total task instruct
############################################################
## SECTION H · Testing
############################################################
13. Add tests to validate:
      • train_model.py outputs model.pkl
      • API returns 200 and valid JSON
      • utils compute_kappa() > 0 on dummy data

# END OF SCRIPT
