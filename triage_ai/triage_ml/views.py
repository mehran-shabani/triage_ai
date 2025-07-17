import joblib
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TriageRequestSerializer, TriageResponseSerializer
from .models import CaseLog

MODEL_PATH = Path(__file__).resolve().parent / 'ml_pipeline/artifacts/model.pkl'


class PredictView(APIView):
    def post(self, request):
        serializer = TriageRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            features = [[data['Age'], data['SBP'], data['DBP'], data['HR'], data['RR'], data['BT'], data['SpO2']]]
            ktas = int(model.predict(features)[0])
        else:
            ktas = 3  # default

        flag = None
        if ktas >= 4 and data['NRS_pain'] >= 7 and data['Pain_axis'] == 'central':
            ktas = 3
            flag = 'NEED-RN-REVIEW'

        CaseLog.objects.create(
            pid=data.get('pid'),
            input_features=data,
            ktas_predicted=ktas,
            ktas_expert=data.get('KTAS_expert'),
            is_error=data.get('KTAS_expert') not in (None, ktas),
        )

        resp = {'ktas_predicted': ktas, 'flag': flag}
        return Response(TriageResponseSerializer(resp).data, status=status.HTTP_200_OK)
