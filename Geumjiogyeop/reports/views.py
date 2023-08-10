from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Report
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportBaseModelSerializer
User = get_user_model()

# Create your views here.

class ReportModelViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportBaseModelSerializer

    def create(self, request):
        serializer = ReportBaseModelSerializer(data=request.data)
        victim_id = request.data['victim_id'][1:]
        print('@@@@@@@@@',victim_id)
        try:
            user = User.objects.get(pk = victim_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(victim = user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)