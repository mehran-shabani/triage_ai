from triage_ai.triage_ml.output import prediction_to_message


def test_prediction_message():
    assert "KTAS level 3" in prediction_to_message(3)
    assert "NEED-RN-REVIEW" in prediction_to_message(3, "NEED-RN-REVIEW")
