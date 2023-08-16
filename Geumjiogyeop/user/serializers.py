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
    identifier = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # fields = ['user_id', 'phonenumber', 'password']
        fields = ['identifier', 'password']

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if identifier.isdigit() and len(identifier) >= 11:
            user = User.objects.filter(phonenumber=identifier).first()
        else:
            # user_id = int(identifier) - 1000 # 1001과 같은 값으로 로그인할 수 있도록
            user = User.objects.filter(user_id=identifier).first()

        if user is None:
            raise serializers.ValidationError('User does not exist.')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # user = User.objects.create_user(
        #     user_id = validated_data['user_id'],
        #     phonenumber = validated_data['phonenumber'],
        #     password = validated_data['password']
        # )
        user = validated_data['user']
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

# user가 등록한 adoption 글 list(register-adoption용) 및 count 조회(my용)용 시리얼라이저
class UserAdoptionListSerializer(serializers.ModelSerializer):
    adoptions = AdoptionSerializer(many=True)
    adoptions_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'name', 'adoptions', 'adoptions_count']

    def get_adoptions_count(self, obj):
        return obj.adoptions.count()

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