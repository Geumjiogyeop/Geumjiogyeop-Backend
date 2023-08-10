from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class PostModelViewSet(ModelViewSet):
    queryset = Today.objects.all()
    serializer_class = PostListModelSerializer