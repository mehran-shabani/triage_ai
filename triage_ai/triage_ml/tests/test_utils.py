from triage_ai.triage_ml.utils import compute_kappa, compute_pearson


def test_utils():
    y_true = [1, 2, 3]
    y_pred = [1, 2, 2]
    assert compute_kappa(y_true, y_pred) <= 1
    assert -1 <= compute_pearson(y_true, y_pred) <= 1
