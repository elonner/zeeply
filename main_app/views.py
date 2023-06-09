from typing import Any, Dict
from django.db.models.query import QuerySet
from django.db.models import Func, IntegerField, F, Case, When
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.widgets import AdminDateWidget
from .models import Skill, Post, Profile, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
# from .forms import PostForm
import uuid
import boto3
import os
from .models import File
from django.urls import reverse

 
# Create your views here.
class HomeFeedList(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_list = Skill.objects.all()
        context['skill_list'] = skill_list
        context['is_explore_page'] = True
        return context
    
    def get_queryset(self):
        if bool(self.request.GET):
            skill_name = self.request.GET.get('filter')
            filter_skill = Skill.objects.filter(skill=skill_name)
            return Post.objects.filter(skill__in=filter_skill)
        return Post.objects.all()
            

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
    
class GetPoints(Func):
    function = 'get_points'
    output_field = IntegerField()
    
class SearchList(ListView):
    model = Post
    
    def get_queryset(self):
        if bool(self.request.GET):
            keywords = self.request.GET.get('searchInput').split()
            posts = Post.objects.all()
            result_list = []
            id_list = []
            def point_value(elem):
                return elem[1]
            for p in posts:
                points = p.get_points(keywords)
                if points > 0: result_list.append((p.id, points))
            result_list.sort(key=point_value, reverse=True)
            for result in result_list:
                id_list.append(result[0])
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(id_list)])
            queryset = Post.objects.filter(pk__in=id_list).order_by(preserved)[:20]
            return queryset
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_search_page'] = True
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


class PostForm(forms.ModelForm):
    file = forms.FileField()
    class Meta:
        model = Post
        fields = ['title', 'description', 'header', 'contentBlock', 'skill', 'file']

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # success_url = 'posts/{pk}/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['skill'].queryset = Skill.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user

        # Save the post before saves to database 
        post = form.save(commit=False)

        # Get the uploaded file from the form's cleaned data
        media_file = form.cleaned_data.get('file') 

        if media_file:
            # Generate a unique key for the file in S3
            key = f"posts/{uuid.uuid4().hex}/{media_file.name}"

            # Uploading to AWS
            s3 = boto3.client('s3')
            s3.upload_fileobj(media_file, os.environ['S3_BUCKET'], key)

            # Save the post object to the database
            post.save()

            # Create a File object and associate it with the post
            file_obj = File.objects.create(url=f"{os.environ['S3_BASE_URL']}/{os.environ['S3_BUCKET']}/{key}", post=post)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('posts_detail', kwargs={'pk': self.object.pk})
    

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(post=self.kwargs.get('pk'))
        context['reviews'] = reviews

         # Get the associated pictures/files for the post
        files = File.objects.filter(post=self.object)
        context['files'] = files

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
        if bool(self.request.GET):
            skill_name = self.request.GET.get('filter')
            filter_skill = Skill.objects.filter(skill=skill_name)
            return Post.objects.filter(skill__in=filter_skill).filter(savedBy=user)
        return Post.objects.filter(savedBy=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_list = Skill.objects.all()
        context['skill_list'] = skill_list
        context['is_saved_page'] = True
        return context
    
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
    return redirect('/', post_id)

def unsave_post(request, post_id):
    Post.objects.get(id=post_id).savedBy.remove(request.user.id)
    return redirect('/', post_id)

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
            return redirect('profiles_create')
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

class ProfileUpdate (LoginRequiredMixin, UpdateView):
  model = Profile
  fields = ['phone', 'bio']


class UsersDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'main_app/user_detail.html'
    context_object_name = 'curr_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.kwargs.get('pk'))
        skill_list = Skill.objects.filter(user=self.kwargs.get('pk'))
        if bool(self.request.GET):
            skill_name = self.request.GET.get('filter')
            filter_skill = Skill.objects.filter(skill=skill_name).get(user=self.kwargs.get('pk'))
            post_list = Post.objects.filter(skill=filter_skill).filter(creator=self.kwargs.get('pk'))
        else:
            post_list = Post.objects.filter(creator=self.kwargs.get('pk'))
        context['profile'] = profile
        context['post_list'] = post_list
        context['skill_list'] = skill_list
        return context


def add_photo(request, post_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            
            post = Post.objects.get(id=post_id)
            # we can assign to cat_id or cat (if you have a cat object)
            Post.objects.create(url=url, post=post)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('post_detail', pk=post_id)