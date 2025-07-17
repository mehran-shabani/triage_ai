from django.db import models
from django.db.models import JSONField


class CaseLog(models.Model):
    pid = models.CharField(max_length=64, blank=True, null=True)
    input_features = JSONField()
    ktas_predicted = models.IntegerField()
    ktas_expert = models.IntegerField(blank=True, null=True)
    is_error = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case {self.pid}"
