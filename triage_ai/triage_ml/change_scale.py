SCORE_MAP = {
    "no pain": 0,
    "dull": 2,
    "mild": 3,
    "moderate": 5,
    "throbbing": 6,
    "severe": 8,
    "agonizing": 10,
}


def text_to_score(text):
    """Convert a descriptive pain phrase into an NRS value."""
    return SCORE_MAP.get(text.lower())


def score_to_text(score):
    """Convert an NRS score into a descriptive term."""
    nearest = min(SCORE_MAP.items(), key=lambda x: abs(score - x[1]))[0]
    return nearest
