from rest_framework import serializers

from user.models import User
from .models import Adoption, UserLikedAdoption

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AdoptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['adoption_id', 'name', 'gender', 'age', 'center', 'introduction', 'photo', 'likes']

class AdoptionCreateSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Adoption
        fields = ['adoption_id', 'name', 'breed', 'gender', 'age', 'weight', 
                  'is_neutralized', 'center', 'introduction', 'letter', 'photo', 'created_at'] # , 'user'
    
    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        return super().create(validated_data)

class AdoptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        # fields = ['adoption_id', 'user', 'name', 'breed', 'gender', 'age', 'weight', 
        #           'is_neutralized', 'center', 'introduction', 'letter', 'photo', 'likes', 'contact_num']
        fields = ['adoption_id', 'name', 'breed', 'gender', 'age', 'weight', 
            'is_neutralized', 'center', 'introduction', 'letter', 'photo', 'likes', 'contact_num']