from django.contrib import admin
from .models import Today, Images

# Register your models here.
@admin.register(Today)
class TodayModelAdmin(admin.ModelAdmin):
    pass

@admin.reister(Images)
class ImageModelAdmin(admin.ModelAdmin):
    pass