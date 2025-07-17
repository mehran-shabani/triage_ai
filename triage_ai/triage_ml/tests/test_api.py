from django.urls import reverse
from rest_framework.test import APIClient


def test_predict_endpoint(db):
    client = APIClient()
    payload = {
        "Age": 71,
        "Sex": "Male",
        "SBP": 160,
        "DBP": 100,
        "HR": 84,
        "RR": 18,
        "BT": 37.4,
        "SpO2": 98,
        "NRS_pain": 8,
        "Pain_axis": "central",
        "Chief_complain": "test",
        "Arrival_mode": "walk-in",
        "KTAS_expert": 3
    }
    url = reverse('triage-predict')
    response = client.post(url, payload, format='json')
    assert response.status_code == 200
    assert 'ktas_predicted' in response.data
