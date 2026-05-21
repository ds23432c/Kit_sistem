from django.contrib import admin
from .models import AccountingReport

@admin.register(AccountingReport)
class AccountingReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at']
