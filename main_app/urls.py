from django.urls import path
from . import views

urlpatterns = [
    # home (for now)
    path('', views.HomeFeedList.as_view(), name="home_feed_list"),
    # home - following
    path('following/', views.FollowingPosts.as_view(), name="following_posts"),
    # sign up
    path('accounts/signup/', views.signup, name='signup'),
    # PROFILE - create
    path('profiles/create/', views.ProfileCreate.as_view(), name='profiles_create'),
    
    #PROFILE - update
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profiles_update'),

    # USER - detail
    path('users/<int:pk>/', views.UsersDetail.as_view(), name='users_detail'),
    # USER - follow
    path('users/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    # USER - unfollow
    path('users/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    # SKILL - create
    path('skills/create/', views.SkillCreate.as_view(), name='skills_create'),
    # SKILL - update
    path('skills/<int:pk>/update/', views.SkillUpdate.as_view(), name='skills_update'),
    # SKILL - delete
    path('skills/<int:pk>/delete/', views.SkillDelete.as_view(), name='skills_delete'),
    # POST - create
    path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    # POST - detail
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='posts_detail'),
    # POST - update
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    # POST - delete
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
    # POST - save
    path('posts/<int:post_id>/save/', views.save_post, name='posts_save'),
    # POST - unsave
    path('posts/<int:post_id>/unsave/', views.unsave_post, name='posts_unsave'),
    # POST - saved posts
    path('posts/saved/', views.SavedList.as_view(), name='saved_list'),
    # REVIEW - create
    path('posts/<int:post_id>/reviews/create/', views.ReviewCreate.as_view(), name='reviews_create'),
    # REVIEW - update
    path('posts/<int:post_id>/reviews/<int:pk>/update/', views.ReviewUpdate.as_view(), name='reviews_update'),
    # REVIEW - delete
    path('posts/<int:post_id>/reviews/<int:pk>/delete/', views.ReviewDelete.as_view(), name='reviews_delete'),

]