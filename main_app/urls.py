from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/signup', views.signup, name='signup'),
    path('skills/create', views.SkillCreate.as_view(), name='skills_create'),
]