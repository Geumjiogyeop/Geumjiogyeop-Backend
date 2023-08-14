from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Adoption, UserLikedAdoption
from .serializers import AdoptionListSerializer, AdoptionCreateSerializer, AdoptionDetailSerializer

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

class AdoptionCreate(generics.CreateAPIView):
    queryset= Adoption.objects.all()
    serializer_class= AdoptionCreateSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, *args, **kwargs):
        serializer = AdoptionCreateSerializer(data=request.data)

        if serializer.is_valid():
            # adoption = Adoption.objects.create(
            # )
            # serializer.validated_data['user'] = self.request.user
            adoption = serializer.save()
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdoptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Adoption.objects.all()
    serializer_class= AdoptionDetailSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
        # if kwargs.get('update'):
        #     # serializer = AdoptionDetailSerializer(data=request.data)
        #     serializer = self.get_serializer(self.get_object(), data=request.data)

        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        # if kwargs.get('delete'):
        #     instance = self.get_object()
        #     instance.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # return Response(status=status.HTTP_400_BAD_REQUEST)

class AdoptionLikeView(generics.GenericAPIView):
    queryset = Adoption.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        # user = request.user

        # like, created = UserLikedAdoption.objects.get_or_create(user=user, adoption=instance)
        # if created:
        instance.likes += 1
        instance.save()
        return Response(instance.likes)

class AdoptionCancelLikeView(generics.GenericAPIView):
    queryset = Adoption.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.likes -= 1
        instance.save()
        return Response(instance.likes)