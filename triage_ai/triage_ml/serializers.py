from rest_framework import serializers


class TriageRequestSerializer(serializers.Serializer):
    pid = serializers.CharField(required=False, allow_blank=True)
    Age = serializers.IntegerField()
    Sex = serializers.ChoiceField(choices=['Male', 'Female'])
    SBP = serializers.IntegerField()
    DBP = serializers.IntegerField()
    HR = serializers.IntegerField()
    RR = serializers.IntegerField()
    BT = serializers.FloatField()
    SpO2 = serializers.IntegerField()
    NRS_pain = serializers.IntegerField()
    Pain_axis = serializers.ChoiceField(choices=['central', 'peripheral'])
    Chief_complain = serializers.CharField(max_length=120)
    Arrival_mode = serializers.CharField()
    KTAS_expert = serializers.IntegerField(required=False)


class TriageResponseSerializer(serializers.Serializer):
    ktas_predicted = serializers.IntegerField()
    flag = serializers.CharField(allow_null=True)
