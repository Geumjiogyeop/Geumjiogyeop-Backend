from rest_framework import serializers

from user.models import User
from .models import Adoption, UserLikedAdoption
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# 로그인 안 한 user도 볼 수 있음
class AdoptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['adoption_id', 'name', 'gender', 'age', 'center', 'introduction', 'photo', 'likes']

# 로그인된 user만 볼 수 있음
class AdoptionLikedListSerializer(serializers.ModelSerializer):
    isLike = serializers.SerializerMethodField()

    class Meta:
        model = Adoption
        fields = ['adoption_id', 'name', 'gender', 'age', 'center', 'introduction', 'photo', 'likes', 'isLike']

    def get_isLike(self, obj):
        try:
            # token = self.context.COOKIES.get('jwt')
            token = self.context['request'].COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')

            user = User.objects.get(user_id=payload['user_id'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        try: 
            UserLikedAdoption.objects.get(adoption = obj, user = user)
        except UserLikedAdoption.DoesNotExist:
            return False
        return True

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