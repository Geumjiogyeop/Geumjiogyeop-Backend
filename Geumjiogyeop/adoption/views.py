from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Adoption, UserLikedAdoption
from user.models import User
from .serializers import AdoptionListSerializer, AdoptionCreateSerializer, AdoptionDetailSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings

# adoption list 필터링 적용
class AdoptionList(generics.ListAPIView):
    serializer_class = AdoptionListSerializer

    def get_queryset(self):
        queryset = Adoption.objects.all()
        params = self.request.query_params

        adoption_availability = params.getlist('adoption_availability')
        # center = params.getlist('center')
        center = params.get('center')
        breed = params.getlist('breed')
        gender = params.getlist('gender')
        age = params.getlist('age')

        if adoption_availability:
            queryset = queryset.filter(adoption_availability__in=adoption_availability)
        if center:
            # queryset = queryset.filter(center__in=center)
            queryset = queryset.filter(center__icontains=center) # 해당 문자열 포함하는 모든 레코드 get
        if breed:
            queryset = queryset.filter(breed__in=breed)
        if gender:
            queryset = queryset.filter(gender__in=gender)
        if age:
            queryset = queryset.filter(age__in=age)

        return queryset

# adoption 글 create - 로그인한 user만 create 가능
class AdoptionCreate(generics.CreateAPIView):
    queryset= Adoption.objects.all()
    serializer_class= AdoptionCreateSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        try:
            token = request.COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(user_id=payload['user_id'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found.')
            
            serializer = AdoptionCreateSerializer(data=request.data, context={'user': user})

            if serializer.is_valid():
                adoption = serializer.save()
            
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

# adoption detail 상세정보 get, patch, delete
class AdoptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Adoption.objects.all()
    serializer_class= AdoptionDetailSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# adoption에 좋아요 누르기 - 로그인한 user만 가능
class AdoptionLikeView(generics.GenericAPIView):
    queryset = Adoption.objects.all()

    def get_object(self):
        adoption_id = self.kwargs.get('pk')
        return generics.get_object_or_404(Adoption, pk=adoption_id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            # 이미 좋아요를 눌렀었는지 확인
            liked_adoption = UserLikedAdoption.objects.filter(user_id=user_id, adoption=instance).first()
            if liked_adoption:
                return Response({'detail': 'You have already liked this adoption.'}, status=status.HTTP_400_BAD_REQUEST)

            # UserLikedAdoption 모델에 저장
            user_liked_adoption = UserLikedAdoption(user_id=user_id, adoption=instance)
            user_liked_adoption.save()

            # likes 값 증가
            instance.likes += 1
            instance.save()

            return Response({'detail': 'Adoption liked successfully.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

# adoption에 좋아요 취소하기 - 로그인한 user만 가능
class AdoptionCancelLikeView(generics.GenericAPIView):
    queryset = Adoption.objects.all()
    
    def get_object(self):
        adoption_id = self.kwargs.get('pk')
        return generics.get_object_or_404(Adoption, pk=adoption_id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']  # Assuming 'user_id' is in the payload

            # 이미 좋아요를 눌렀었는지 확인
            liked_adoption = UserLikedAdoption.objects.filter(user_id=user_id, adoption=instance).first()
            if not liked_adoption:
                return Response({'detail': 'You have not liked this adoption.'}, status=status.HTTP_400_BAD_REQUEST)

            # UserLikedAdoption 모델에서 해당되는 like 레코드 삭제
            liked_adoption.delete()

            # likes 값 감소
            instance.likes -= 1
            instance.save()

            return Response({'detail': 'Like canceled successfully.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')