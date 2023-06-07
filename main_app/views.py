from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.widgets import AdminDateWidget
from .models import Skill, Post, Profile, Review
from django.contrib.auth.models import User

 
# Create your views here.
class HomeFeedList(ListView):
    model = Post


class FollowingPosts(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        curr_user_prof = Profile.objects.get(user=self.request.user)
        following = curr_user_prof.following.all()
        return Post.objects.filter(creator__in=following)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_following_page'] = True
        return context

class SkillCreate(LoginRequiredMixin, CreateView): # add ability for experience to be ongoing
    model = Skill
    fields = ['skill', 'description', 'categories', 'startDate', 'endDate', 'isOngoing']

    # override the form_valid method to assign the logged in user, self.request.user
    def form_valid(self, form):
        form.instance.user = self.request.user # form.instance is the skill
        return super().form_valid(form)
    
class SkillUpdate(LoginRequiredMixin, UpdateView):
    model = Skill
    fields = ['description', 'categories', 'startDate', 'endDate', 'isOngoing']

class SkillDelete(LoginRequiredMixin, DeleteView):
    model = Skill 
    success_url = '/'
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'header', 'contentBlock', 'skill']

    def form_valid(self, form):
        form.instance.creator = self.request.user # form.instance is the post
        return super().form_valid(form)
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(post=self.kwargs.get('pk'))
        context['reviews'] = reviews
        return context

#POST - CBV - UPDATE
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'header', 'contentBlock', 'skill']

#POST - CBV - DELETE
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

class SavedList(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(savedBy=user)
    
class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'content']

    def form_valid(self, form):
        form.instance.creator = self.request.user # form.instance is the review
        form.instance.post = Post.objects.get(pk=self.kwargs.get('post_id'))
        return super().form_valid(form)
    
class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = '__all__'

class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = '/'

def follow_user(request, user_id):
    curr_user_prof = Profile.objects.get(user=request.user)
    user_prof = Profile.objects.get(user=user_id)
    curr_user_prof.following.add(User.objects.get(pk=user_id))
    user_prof.followers.add(request.user)
    return redirect('users_detail', user_id)

def unfollow_user(request, user_id):
    curr_user_prof = Profile.objects.get(user=request.user)
    user_prof = Profile.objects.get(user=user_id)
    curr_user_prof.following.remove(User.objects.get(pk=user_id))
    user_prof.followers.remove(request.user)
    return redirect('users_detail', user_id)

def save_post(request, post_id):
    Post.objects.get(id=post_id).savedBy.add(request.user.id)
    return redirect('posts_detail', post_id)

def unsave_post(request, post_id):
    Post.objects.get(id=post_id).savedBy.remove(request.user.id)
    return redirect('posts_detail', post_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['phone', 'bio']

    def form_valid(self, form):
        form.instance.user = self.request.user # form.instance is the finch
        return super().form_valid(form)

class UsersDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'main_app/user_detail.html'
    context_object_name = 'curr_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.kwargs.get('pk'))
        post_list = Post.objects.filter(creator=self.kwargs.get('pk'))
        context['profile'] = profile
        context['post_list'] = post_list
        return context

