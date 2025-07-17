import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from pathlib import Path

from .preprocess import preprocess
from ..utils import compute_kappa, compute_pearson

DATA_PATH = Path(__file__).resolve().parents[3] / 'data/triage_data.csv.csv'
ARTIFACT_PATH = Path(__file__).resolve().parent / 'artifacts/model.pkl'


def train():
    df = pd.read_csv(DATA_PATH, sep=';')
    df = preprocess(df)
    X = df[['Age', 'SBP', 'DBP', 'HR', 'RR', 'BT', 'SpO2']]
    y = df['KTAS_expert']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    param_grid = {'n_estimators': [100, 300], 'max_depth': [None, 10]}
    search = GridSearchCV(RandomForestClassifier(class_weight='balanced_subsample'), param_grid, cv=3, n_jobs=-1)
    search.fit(X_train, y_train)
    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print('Weighted Kappa:', compute_kappa(y_test, y_pred))
    print('Pearson r:', compute_pearson(y_test, y_pred))
    print('Confusion:\n', confusion_matrix(y_test, y_pred))
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, ARTIFACT_PATH)


if __name__ == '__main__':
    train()
