from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Today(models.Model):
    title = models.TextField("제목")
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성날짜", auto_now_add=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

class Images(models.Model):
    today_id = models.ForeignKey(to=Today, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(verbose_name="이미지", null = True, blank=True)