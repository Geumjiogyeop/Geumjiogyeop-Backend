from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Report

class ReportBaseModelSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        depth = 1