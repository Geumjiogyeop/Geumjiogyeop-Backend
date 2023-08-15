from django.urls import include, path
from .views import *

urlpatterns = [
    path("", AdoptionList.as_view()),
    path("create", AdoptionCreate.as_view()),
    path("<int:pk>", AdoptionDetail.as_view()),
    path("<int:pk>/likes", AdoptionLikeView.as_view()),
    path("<int:pk>/cancellikes", AdoptionCancelLikeView.as_view()),
]