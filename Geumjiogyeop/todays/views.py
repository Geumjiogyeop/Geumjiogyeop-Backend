from django.conf import settings
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Today, TodayLiked
from user.models import User
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import TodayImageSerializer, TodaySerializer, TodayRetrieveSerializer, TodayLikedSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt
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
        try:
            token = request.COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')

            user = User.objects.get(user_id=payload['user_id'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        todays = Today.objects.filter(writer = user)
        serializer = TodaySerializer(todays, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        try:
            token = request.COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')

            user = User.objects.get(user_id=payload['user_id'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        instance = self.get_object()
        if TodayLiked.objects.filter(user = user, today = instance).exists():
            instance.likes -= 1
            instance.save()
            TodayLiked.objects.filter(user = user, today = instance).delete()
        else:
            instance.likes += 1
            instance.save()
            data = {"user": user.user_id, "today" : instance.id}

            serializer = TodayLikedSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return Response(status = status.HTTP_200_OK)