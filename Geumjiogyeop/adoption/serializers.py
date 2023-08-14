from rest_framework import serializers

from user.models import User
from .models import Adoption, UserLikedAdoption

class AdoptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['name', 'gender', 'age', 'center', 'introduction', 'photo', 'likes']

class AdoptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['name', 'breed', 'gender', 'age', 'weight', 
                  'is_neutralized', 'center', 'introduction', 'letter', 'photo']

class AdoptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        # fields = ['adoption_id', 'user', 'name', 'breed', 'gender', 'age', 'weight', 
        #           'is_neutralized', 'center', 'introduction', 'letter', 'photo', 'likes', 'contact_num']
        fields = ['adoption_id', 'name', 'breed', 'gender', 'age', 'weight', 
            'is_neutralized', 'center', 'introduction', 'letter', 'photo', 'likes', 'contact_num']