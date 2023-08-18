from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from adoption.models import Adoption, UserLikedAdoption
from todays.models import Today
from .serializers import *
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from adoption.serializers import AdoptionListSerializer
from todays.serializers import TodayListModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
import jwt, datetime
# from jwt.exceptions import ExpiredSignatureError, ImmatureSignatureError
from datetime import datetime, timedelta, timezone

# 회원가입
class UserRegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    def post(self, req):
        serializer = UserRegisterSerializer(data=req.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # print('serializer:', req.data)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 로그인
class UserLoginView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    def post(self,req):
        # phonenumber = req.data['phonenumber']
        # password = req.data['password']

        # user = User.objects.filter(phonenumber=phonenumber).first()
        # serialize_user = UserLoginSerializer(user)
        # json_user = JSONRenderer().render(serialize_user.data)

        serializer = UserLoginSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if user is None :
            raise AuthenticationFailed('User does not found!')
        
        current_time = datetime.now(timezone.utc)
        expiration_time = current_time + timedelta(minutes=60)

        ## JWT 구현 부분
        payload = {
            'user_id' : int(user.user_id), # KeyError 발생 때문에 'user_id'로 변경
            'exp' : expiration_time,
            'iat' : current_time
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256") # .decode("utf-8")

        res = Response()
        res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'jwt' : token
        }
        return res
    
# 로그아웃
class UserLogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self,req):
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        res = Response()
        res.delete_cookie('jwt')
        res.data = {
            "message" : 'success'
        }
        return res
    
class UserDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get(self,req):
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.get(user_id=payload['user_id'])
        # user = User.objects.get(user_id=payload['user_id']).first()
        
        serializer = UserDetailSerializer(user)

        return Response(serializer.data)

    # account 수정 시
    def put(self,req): # pk 추가
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.get(user_id=payload['user_id'])
        serializer = UserAdoptionDetailSerializer(user, data=req.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# user가 등록한 입양공고 list 조회
class UserAdoptionListView(APIView):
    def get(self, request): # , pk
        try:
            token = request.COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')

            user = User.objects.get(user_id=payload['user_id'])

            serializer = UserAdoptionListSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
# user가 등록한 입양공고 detail 조회
class UserAdoptionDetailView(APIView):
    def get(self, request, adoption_pk): # , pk
        try:
            token = request.COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')

            user = User.objects.get(user_id=payload['user_id'])

            # user = User.objects.get(user_id=pk)
            # adoption = Adoption.objects.get(adoption_id=adoption_pk, user_id=user)
            # serializer = UserAdoptionDetailSerializer(user)
            serializer = UserAdoptionDetailSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Adoption.DoesNotExist:
            return Response({"error": "Adoption not found for the given user."}, status=status.HTTP_404_NOT_FOUND)

# user 관심공고 list 조회   
class UserLikedAdoptionListView(generics.ListAPIView):
    serializer_class = LikedAdoptionSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return UserLikedAdoption.objects.filter(user=payload['user_id'])
    
class MainView(APIView):
    serializer_class = [AdoptionListSerializer, TodayListModelSerializer]
    
    def get(self,req):
        queryset = Adoption.objects.all()
        serializer = AdoptionListSerializer(queryset,many=True)
        print("dfjsdfskd", serializer.data)
        adoption = serializer.data
        print("adkfsljfkd")
        queryset = Today.objects.all()
        serializer = TodayListModelSerializer(queryset, many=True)
        today = serializer.data
        print("dfksdfl")
        return Response({"adoption" : adoption, "today" : today})


