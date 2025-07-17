from sklearn.metrics import cohen_kappa_score
from scipy.stats import pearsonr


def compute_kappa(y_true, y_pred):
    return cohen_kappa_score(y_true, y_pred, weights='quadratic')


def compute_pearson(x, y):
    r, _ = pearsonr(x, y)
    return r
