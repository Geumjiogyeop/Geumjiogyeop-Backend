from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Today)
class TodayModelAdmin(admin.ModelAdmin):
    pass