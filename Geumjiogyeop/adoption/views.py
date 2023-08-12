from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Adoption, UserLikedAdoption
from .serializers import AdoptionListSerializer, AdoptionCreateSerializer, AdoptionDetailSerializer

class AdoptionList(generics.ListAPIView):
    # queryset= Adoption.objects.all()
    serializer_class = AdoptionListSerializer
    # filter_backends = [filters.SearchFilter]
    # '^' : starts-with search, '=' : exact matches, '@' : full-text search, '$' : regax search
    # search_fields = ['=adoption_availability', 'center', 'breed', '=gender', '=age']
    def get_queryset(self):
        queryset = Adoption.objects.all()
        adoption_availability = self.request.query_params.get('adoption_availability', None)
        center = self.request.query_params.get('center', None)
        breed = self.request.query_params.get('breed', None)
        gender = self.request.query_params.get('gender', None)
        age = self.request.query_params.get('age', None)
        if adoption_availability is not None:
            queryset = queryset.filter(adoption_availability=adoption_availability)
        if center is not None:
            queryset = queryset.filter(center=center)
        if breed is not None:
            queryset = queryset.filter(breed=breed)
        if gender is not None:
            queryset = queryset.filter(gender=gender)
        if age is not None:
            queryset = queryset.filter(age=age)
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