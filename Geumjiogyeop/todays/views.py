from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Today
from .serializers import TodayImageSerializer, TodaySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class TodayViewSet(ModelViewSet):
    queryset = Today.objects.all().order_by('-created_at')
    serializer_class = TodaySerializer