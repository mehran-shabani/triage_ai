from triage_ai.triage_ml.change_scale import text_to_score, score_to_text


def test_change_scale_mapping():
    assert text_to_score("throbbing") == 6
    assert score_to_text(10) == "agonizing"
