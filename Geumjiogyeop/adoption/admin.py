from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Adoption)
class AdoptionModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserLikedAdoption)
class UserLikedAdoptionModelAdmin(admin.ModelAdmin):
    pass