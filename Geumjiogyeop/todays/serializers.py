import os
from django.conf import settings
from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Today, Images
from rest_framework.fields import CurrentUserDefault

class TodayImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Images
        fields = ['image']


class TodaySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

	#게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all() 
        return TodayImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Today
        fields = '__all__'

    def create(self, validated_data):
        instance = Today.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        if self.context['request'].user.is_authenticated:
            for image_data in image_set.getlist('image'):
                Images.objects.create(today=instance, image=image_data, writer = self.context['request'].user)
        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        image_delete = Images.objects.filter(today = instance)
        for image in image_delete:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.id), image.image.path))
            print("삭제@@@@@@@@")
        image_delete.delete()
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Images.objects.create(today=instance, image=image_data)
        return instance
    
class TodayRetrieveSerializer(serializers.ModelSerializer):
    editable = serializers.SerializerMethodField()
    class Meta:
        model = Today
        fields = ['title', 'writer', 'content', 'created_at', 'editable']
        depth = 1

    def get_editable(self, obj):
        print("Current@@@@@@@@", self.context.user)
        print("writer@@@@@@@", obj.writer)
        if self.context.user == obj.writer:
            return True
        else:
            return False