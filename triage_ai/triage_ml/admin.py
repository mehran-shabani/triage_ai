from django.contrib import admin
from .models import CaseLog


@admin.register(CaseLog)
class CaseLogAdmin(admin.ModelAdmin):
    list_display = ('pid', 'ktas_predicted', 'ktas_expert', 'is_error', 'created_at')
