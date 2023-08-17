import os
from django.conf import settings
from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Today, Images, TodayLiked
from user.models import User
from rest_framework.fields import CurrentUserDefault
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt
from rest_framework.response import Response

class TodayImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Images
        fields = ['image']

class TodaySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    editable = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()

	#게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all()
        return TodayImageSerializer(instance=image, many=True, context=self.context).data
    
    def get_editable(self, obj):
        try:
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
        if user == obj.writer:
            return True
        else:
            return False
        
    def get_isLike(self, obj):
        try:
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
            TodayLiked.objects.get(today = obj, user = user)
        except TodayLiked.DoesNotExist:
            return False
        return True


    class Meta:
        model = Today
        fields = '__all__'
        depth = 1
    
    def create(self, validated_data):
        try:
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
        instance = Today.objects.create(**validated_data, writer = user)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Images.objects.create(today=instance, image=image_data)
        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        image_delete = Images.objects.filter(today = instance)
        for image in image_delete:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.id), image.image.path))
        image_delete.delete()
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Images.objects.create(today=instance, image=image_data)
        return instance
    
class TodayListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()

	#게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        print(self.context.get('request'))
        image = obj.image.all()
        return TodayImageSerializer(instance=image, many=True, context = {'request' : self.context.get('request')}).data
    
    def get_isLike(self, obj):
        try:
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
            TodayLiked.objects.get(today = obj, user = user)
        except TodayLiked.DoesNotExist:
            return False
        return True

    class Meta:
        model = Today
        fields = '__all__'
        depth = 1
    
class TodayRetrieveSerializer(serializers.ModelSerializer):
    editable = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()

    class Meta:
        model = Today
        fields = ['id','title', 'writer', 'content', 'created_at', 'editable', 'likes', 'images', 'isLike']
        depth = 1
        
	#게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = Images.objects.filter(today = obj)
        return TodayImageSerializer(instance=image, many=True).data

    def get_editable(self, obj):
        try:
            token = self.context.COOKIES.get('jwt')

            if not token :
                raise AuthenticationFailed('UnAuthenticated!')

            try :
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('UnAuthenticated!')

            user = User.objects.get(user_id=payload['user_id'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if user == obj.writer:
            return True
        else:
            return False
        
    def get_isLike(self, obj):
        try:
            token = self.context.COOKIES.get('jwt')

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
            TodayLiked.objects.get(today = obj, user = user)
        except TodayLiked.DoesNotExist:
            return False
        return True
        
class TodayLikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodayLiked
        fields = '__all__'

