from pathlib import Path
from triage_ai.triage_ml.ml_pipeline.train_model import ARTIFACT_PATH, train


def test_train_creates_model(tmp_path, monkeypatch):
    monkeypatch.setattr('triage_ml.ml_pipeline.train_model.DATA_PATH', Path('data/triage_data.csv.csv'))
    monkeypatch.setattr('triage_ml.ml_pipeline.train_model.ARTIFACT_PATH', tmp_path / 'model.pkl')
    train()
    assert (tmp_path / 'model.pkl').exists()
