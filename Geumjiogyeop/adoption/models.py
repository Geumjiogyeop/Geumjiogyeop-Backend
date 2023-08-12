from django.db import models
from user.models import User

class Adoption(models.Model):
    adoption_id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    breed = models.CharField(max_length=10)
    gender = models.CharField(max_length=1) # 남(m), 여(f)
    age = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    is_neutralized = models.BooleanField(default=False)
    center = models.CharField(max_length=50)
    introduction = models.CharField(max_length=100)
    letter = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='', default='default_image.png', blank=True)
    likes = models.IntegerField(default=0)
    contact_num = models.IntegerField(default=0)
    adoption_availability = models.BooleanField(default=False)

class UserLikedAdoption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE)