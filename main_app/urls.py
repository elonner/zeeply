from django.urls import path
from . import views

urlpatterns = [
    # home (for now)
    path('', views.HomeFeedList.as_view(), name="home_feed_list"),
    # sign up
    path('accounts/signup/', views.signup, name='signup'),
    # PROFILE - create
    path('profiles/create/', views.ProfileCreate.as_view(), name='profiles_create'),
    # USER - detail
    path('users/<int:pk>/', views.UsersDetail.as_view(), name='users_detail'),
    # SKILL - create
    path('skills/create/', views.SkillCreate.as_view(), name='skills_create'),
    # SKILL - update
    path('skills/<int:pk>/update/', views.SkillUpdate.as_view(), name='skills_update'),
    # POST - create
    path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    #POST - update
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    #POST - delete
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
]