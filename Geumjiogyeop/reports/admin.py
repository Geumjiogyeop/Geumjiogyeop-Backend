from django.contrib import admin
from .models import Report

# Register your models here.
@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    pass