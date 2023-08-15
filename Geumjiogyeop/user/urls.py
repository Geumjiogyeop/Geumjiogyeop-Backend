from django.urls import include, path
from .views import *

urlpatterns = [
    path("signin", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
    path("view/", UserDetailView.as_view()),
    # path("<int:pk>/register-adoption", UserAdoptionListView.as_view()),
    path("register-adoption", UserAdoptionListView.as_view()),
    # path("<int:pk>/register-adoption/<int:adoption_pk>", UserAdoptionDetailView.as_view()),
    path("register-adoption/<int:adoption_pk>", UserAdoptionDetailView.as_view()),
]