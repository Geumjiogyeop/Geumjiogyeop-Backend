from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    RELATION_CHOICES = [
        ("본인","1"),
        ("가족","2"),
        ("기타","3"),
    ]
    name = models.TextField(verbose_name= "사고자성함",default="")
    relation = models.CharField(verbose_name = "관계", max_length=2, choices = RELATION_CHOICES)
    victim = models.ForeignKey(to=User, on_delete = models.CASCADE)
    date = models.DateTimeField("사고날짜")
    type = models.TextField(verbose_name = "유형")
    etc = models.TextField(verbose_name="기타이유", default="")