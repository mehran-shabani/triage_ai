import pandas as pd


VITALS = ['Age', 'SBP', 'DBP', 'HR', 'RR', 'BT', 'SpO2']


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize vitals and create helper columns."""
    df = df.copy().dropna()
    for col in VITALS:
        df[col] = (df[col] - df[col].mean()) / df[col].std()
    bins = [0, 3, 6, 10]
    labels = ['mild', 'moderate', 'severe']
    df['NRS_pain_cat'] = pd.cut(df['NRS_pain'], bins=bins, labels=labels, right=False)
    df['pain_central_severe'] = (df['Pain_axis'] == 'central') & (df['NRS_pain'] >= 7)
    return df
