from django.db import models
from user.models import User
from django.utils import timezone

class Adoption(models.Model):
    adoption_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='adoptions') # 역참조되도록 related_name 추가
    name = models.CharField(max_length=10)
    # breed = models.CharField(max_length=10)
    breed = models.BooleanField(default=False) # 강아지(True), 고양이(False)
    gender = models.CharField(max_length=1) # 남(m), 여(f)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    # is_neutralized = models.BooleanField(default=False)
    is_neutralized = models.IntegerField(default=1) # 중성화 완료(1), 중성화 미완료(0), 중성화 여부 모름(2)
    center = models.CharField(max_length=50, default='미정')
    introduction = models.CharField(max_length=100, blank=True)
    letter = models.CharField(max_length=400, blank=True)
    photo = models.ImageField(upload_to='', default='default_image.png', blank=True)
    likes = models.IntegerField(default=0)
    contact_num = models.IntegerField(default=0)
    adoption_availability = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class UserLikedAdoption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'adoption']