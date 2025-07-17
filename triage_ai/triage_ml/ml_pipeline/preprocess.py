import pandas as pd

def preprocess(df):
    df = df.copy()
    bins = [0, 3, 6, 10]
    labels = ['mild', 'moderate', 'severe']
    df['NRS_pain_cat'] = pd.cut(df['NRS_pain'], bins=bins, labels=labels, right=False)
    df['pain_central_severe'] = (df['Pain_axis'] == 'central') & (df['NRS_pain'] >= 7)
    return df
