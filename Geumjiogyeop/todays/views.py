from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Today
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import TodayImageSerializer, TodaySerializer, TodayRetrieveSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class TodayViewSet(ModelViewSet):
    queryset = Today.objects.all().order_by('-created_at')
    serializer_class = TodaySerializer

    def retrieve(self, request, pk=None):
        queryset = Today.objects.all()
        today = get_object_or_404(queryset, pk=pk)
        serializer = TodayRetrieveSerializer(today, context = request)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my(self, request):
        todays = Today.objects.filter(writer = request.user)
        serializer = TodaySerializer(todays, many=True)
        return Response(serializer.data)