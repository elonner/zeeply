from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.widgets import AdminDateWidget
from .models import Skill, Post, Profile
from django.contrib.auth.models import User

 
# Create your views here.
class HomeFeedList(ListView):
    model = Post

# class FollowingPosts(LoginRequiredMixin, ListView):
#     model = Post

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
        form.instance.creator = self.request.user # form.instance is the finch
        return super().form_valid(form)
    
class PostDetail(LoginRequiredMixin, DetailView):
  model = Post

#POST - CBV - UPDATE
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'header', 'contentBlock', 'skill']

#POST - CBV - DELETE
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

def save_post(request, post_id):
    Post.objects.get(id=post_id).savedBy.add(request.user.id)
    return redirect('home_feed_list')

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

