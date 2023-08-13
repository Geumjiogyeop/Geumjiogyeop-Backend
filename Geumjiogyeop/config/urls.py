"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from user.views import UserRegisterView, UserLoginView, UserLogoutView, UserDetailView, UserAdoptionListView, UserAdoptionDetailView
from adoption.views import AdoptionList, AdoptionCreate, AdoptionDetail, AdoptionLikeView, AdoptionCancelLikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/signin", UserRegisterView.as_view()),
    path("user/login/", UserLoginView.as_view()),
    path("user/logout/", UserLogoutView.as_view()),
    path("user/view/", UserDetailView.as_view()),
    path("user/<int:pk>/register-adoption", UserAdoptionListView.as_view()),
    path("user/<int:pk>/register-adoption/<int:adoption_pk>", UserAdoptionDetailView.as_view()),
    path("adoption/", AdoptionList.as_view()),
    # path("adoption/(?P<adoption_availability>.+)/$", AdoptionList.as_view()),
    # path("adoption/(?P<center>.+)/$", AdoptionList.as_view()),
    # path("adoption/(?P<breed>.+)/$", AdoptionList.as_view()),
    # path("adoption/(?P<gender>.+)/$", AdoptionList.as_view()),
    # path("adoption/(?P<age>.+)/$", AdoptionList.as_view()),
    path("adoption/create", AdoptionCreate.as_view()),
    path("adoption/<int:pk>", AdoptionDetail.as_view()),
    # path("adoption/<int:pk>/update", AdoptionDetail.as_view(action='update')),
    # path("adoption/<int:pk>/delete", AdoptionDetail.as_view(action='delete')),
    path("adoption/<int:pk>/likes", AdoptionLikeView.as_view()),
    path("adoption/<int:pk>/cancellikes", AdoptionCancelLikeView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
