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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.first()
        context['profile'] = profile
        return context

class SkillCreate(LoginRequiredMixin, CreateView): # add ability for experience to be ongoing
    model = Skill
    fields = ['skill', 'description', 'categories', 'startDate', 'endDate', 'isOngoing']

    # override the form_valid method to assign the logged in user, self.request.user
    def form_valid(self, form):
        form.instance.user = self.request.user # form.instance is the skill
        return super().form_valid(form)
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'header', 'contentBlock', 'skill']

    def form_valid(self, form):
        form.instance.creator = self.request.user # form.instance is the finch
        return super().form_valid(form)

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
    
class ProfilesDetail(LoginRequiredMixin, DetailView):
    model = Profile

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     profile = Profile.objects.first()
    #     context['profile'] = profile
    #     return context

