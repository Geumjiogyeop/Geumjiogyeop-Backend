from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Report
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportBaseModelSerializer
User = get_user_model()
from django.shortcuts import render
from django.http import Http404, HttpResponse

def html_form_view(request):
    print("dfksdjfks")
    return render(request, 'index.html')

# Create your views here.

class ReportModelViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportBaseModelSerializer

    def create(self, request):
        serializer = ReportBaseModelSerializer(data=request.data)
        victim_id = request.data['victim_id'][1:]
        try:
            user = User.objects.get(pk = victim_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid(raise_exception=True):
            serializer.save(victim = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status = status.HTTP_404_NOT_FOUND)