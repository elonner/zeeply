from django.urls import path
from . import views

urlpatterns = [
    # home (for now)
    path('', views.HomeFeedList.as_view(), name="home_feed_list"),
    # sign up
    path('accounts/signup', views.signup, name='signup'),
    # PROFILE - create
    path('profiles/create', views.ProfileCreate.as_view(), name='profiles_create'),
    # PROFILE - detail
    path('profiles/<int:pk>', views.ProfileDetail.as_view(), name='profiles_detail'),
    # SKILL - create
    path('skills/create', views.SkillCreate.as_view(), name='skills_create'),
    # POST - create
    path('posts/create', views.PostCreate.as_view(), name='posts_create'),
]