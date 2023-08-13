from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from adoption.models import Adoption
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserDetailSerializer, UserAdoptionDetailSerializer, UserAdoptionListSerializer, AdoptionSerializer
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
import jwt, datetime

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
    
# 로그인
class UserLoginView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    def post(self,req):
        # account = req.data['account']
        # user_id = req.data['user_id']
        phonenumber = req.data['phonenumber']
        password = req.data['password']

        # account_data = None
        # if User.objects.filter(user_id=account).exists():
        #     account_data = User.objects.get(user_id=account)
        #     user = User.objects.filter(user_id=account_data).first()
        # elif User.objects.filter(phonenumber=account).exists():
        #     account_data = User.objects.get(phonenumber=account)
        #     user = User.objects.filter(phonenumber=account_data).first()

        # if user_id is not None:
        #     user = User.objects.filter(user_id=user_id).first()
        # elif phonenumber is not None:
        user = User.objects.filter(phonenumber=phonenumber).first()
        serialize_user = UserLoginSerializer(user)
        json_user = JSONRenderer().render(serialize_user.data)

        if user is None :
            raise AuthenticationFailed('User does not found!')

        # is same?
        if not user.check_password(password) :
            raise AuthenticationFailed("Incorrect password!")

        ## JWT 구현 부분
        payload = {
            'id' : int(user.user_id),
            'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.now()
        }

        # AttributeError: 'str' object has no attribute 'decode' 때문에 decode 부분 삭제하니 정상적으로 동작
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
    
class UserAdoptionListView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(user_id=pk)
            adoptions = Adoption.objects.filter(user_id=user)
            serializer = UserAdoptionListSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UserAdoptionDetailView(APIView):
    def get(self, request, pk, adoption_pk):
        try:
            user = User.objects.get(user_id=pk)
            adoption = Adoption.objects.get(adoption_id=adoption_pk, user_id=user)
            # serializer = UserAdoptionDetailSerializer(user)
            serializer = AdoptionSerializer(adoption)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Adoption.DoesNotExist:
            return Response({"error": "Adoption not found for the given user."}, status=status.HTTP_404_NOT_FOUND)

# class UserRegisterView(APIView):
#     serializer_class = UserRegisterSerializer
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserLoginView(APIView):
#     serializer_class = UserLoginSerializer
#     def post(self, request):
#         id = request.data.get('id')  # 핸드폰 번호 또는 고유번호(user_id)
#         password = request.data.get('password')
        
#         # 입력된 id 값이 '010'으로 시작하면 핸드폰 번호로, 그렇지 않으면 고유번호로 간주하여 로그인
#         if str(id).startswith('010'):
#             user = authenticate(request, phonenumber=id, password=password)
#         else:
#             user = authenticate(request, user_id=id, password=password)
        
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             return Response({"access_token": access_token}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "User does not found!"}, status=status.HTTP_401_UNAUTHORIZED)

# class UserLogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         refresh_token = request.data.get('refresh_token')
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
#         except:
#             return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# class UserDetailView(APIView):
#     serializer_class = UserDetailSerializer
#     def get(self, request):
#         serializer = UserDetailSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
