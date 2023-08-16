from .models import User
from adoption.models import Adoption, UserLikedAdoption
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

# 회원가입용 시리얼라이저
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phonenumber', 'password', 'name', 'birthday', 'gender', 'is_foreigner']

    def create(self, validated_data):
        user = User.objects.create_user(
            phonenumber = validated_data['phonenumber'],
            password = validated_data['password'],
            # name=validated_data.get('name', ''),
            name = validated_data['name'],
            birthday = validated_data['birthday'],
            gender = validated_data['gender'],
            is_foreigner = validated_data['is_foreigner']
        )
        # print('validate:', validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user

# 로그인용 시리얼라이저
class UserLoginSerializer(serializers.ModelSerializer):
    # account = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['user_id', 'phonenumber', 'password']
        # fields = ['account', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            user_id = validated_data['user_id'],
            phonenumber = validated_data['phonenumber'],
            password = validated_data['password']
        )
        return user

# 계정 확인용 시리얼라이저
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'phonenumber', 'name', 'birthday', 'gender', 'is_foreigner']

class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = '__all__'

# user가 등록한 adoption 글 list 조회용 시리얼라이저
class UserAdoptionListSerializer(serializers.ModelSerializer):
    adoptions = AdoptionSerializer(many=True)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'adoptions']

# user가 등록한 adoption 글 detail 조회용 시리얼라이저
class UserAdoptionDetailSerializer(serializers.ModelSerializer):
    adoptions = AdoptionSerializer(many=True)

    class Meta:
        model = User
        fields = ['adoptions']

# 관심공고 조회 관련 시리얼라이저1
class LikedAdoptionSerializer(serializers.ModelSerializer):
    adoption = AdoptionSerializer()

    class Meta:
        model = UserLikedAdoption
        fields = ['adoption']

# 관심공고 조회 관련 시리얼라이저2
class UserLikedAdoptionSerializer(serializers.ModelSerializer):
    liked_adoptions = LikedAdoptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'liked_adoptions']