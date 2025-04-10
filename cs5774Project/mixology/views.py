import copy
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import *
from django.contrib.auth.models import User

# Create your views here.

nav_urls = [
    {'href': '/', 'name': 'Home', 'active': False, 'icon': 'home.svg'},
    {'href': '/add-drink', 'name': 'New Post', 'active': False, 'icon': 'new-post.svg'},
    {'href': '/profile', 'name': 'Profile', 'active': False, 'icon': 'profile.svg'},
    {'href': '/collections', 'name': 'Collections', 'active': False, 'icon': 'collections.svg'},
    {'href': '/settings', 'name': 'Settings', 'active': False, 'icon': 'settings.svg'},
]

# sign up
def signup(request):
    context = {
        'nav_urls': nav_urls,
    }
    return render(request, 'mixology/signup.html', context)

def process_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Create a user profile
        profile = UserProfile(user=user)
        profile.save()
        
        messages.add_message(request, messages.SUCCESS, 'Account created successfully for %s!' % username)
        
        # Log user in and redirect to the home page
        return redirect('mixology:home')
    
    return signup(request)

# login/logout
def process_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('mixology:home')
    else:
        return redirect('/')

# clear out session vars upon logout
def logout(request):
    request.session.flush()
    return redirect('/')

# home
class IndexView(generic.ListView):
    template_name = 'mixology/index.html'
    context_object_name = 'feed_drinks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[0]['active'] = True
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context

    def get_queryset(self):
        drinks = Drink.objects.filter(status=Drink.Status.PUBLISHED).order_by('-last_updated')
        return sorted(drinks, key=lambda drink: drink.last_updated, reverse=True)

# drink logic

class DrinkView(generic.DetailView):
    model = Drink
    template_name = 'mixology/drink.html'
    context_object_name = 'drink'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        drink_id = self.kwargs.get('did')
        return Drink.objects.get(pk=drink_id)

def add_drink(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.user.is_authenticated:
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('user')
    else:
        return redirect('/')
    active_nav_urls[1]['active'] = True
    
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/add-drink.html', context)

def edit_drink(request, slug):
    active_nav_urls = copy.deepcopy(nav_urls)
    if not request.user.is_authenticated:
        return redirect('/')
    
    drink = [drink for drink in drinks if drink.slug == slug][0]
    
    context = {
        'nav_urls': active_nav_urls,
        'drink': drink,
    }
    return render(request, 'mixology/edit-drink.html', context)

def delete_drink(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.session.get('role') == 'admin' and request.POST.get('submit') == 'delete':
        # TODO: delete drink
        return redirect('/profile/' + request.session.get('user'))
    else:
        return redirect('/')
    

def save_drink(request):
    # TODO: update drink
    drink = [drink for drink in drinks if drink.slug == request.POST.get('slug')][0]
    req_type = request.POST.get('submit')
    if req_type == 'delete' and request.session.get('role') == 'admin':
        active_nav_urls = copy.deepcopy(nav_urls)
        if request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + request.session.get('user')
        context = {
            'nav_urls': active_nav_urls,
            'drink': drink,
        }
        return render(request, 'mixology/delete-drink.html', context)
    elif req_type == 'update':
        return redirect('/drink/' + drink.slug)
    else:
        return redirect('/')

# profile
class ProfileView(generic.DetailView):
    model = UserProfile
    template_name = 'mixology/profile.html'
    context_object_name = 'viewuser'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[2]['active'] = True
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        username = self.kwargs.get('username')
        try:
            user = User.objects.get(username=username)
            print(UserProfile.objects.get(user=user))
            print(user)
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

# about
def about(request):
    active_nav_urls = copy.deepcopy(nav_urls)
        
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/about.html', context)

def contact(request):
    active_nav_urls = copy.deepcopy(nav_urls)
        
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/contact.html', context)

# collections
class CollectionView(generic.ListView):
    model = Collection
    template_name = 'mixology/collections.html'
    context_object_name = 'collections'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[3]['active'] = True
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_queryset(self):
        collections = self.request.user.collections.all()
        return collections

# settings logic
def settings(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    active_nav_urls[4]['active'] = True
    if request.user.is_authenticated:
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('user')
    else:
        return redirect('/')
    
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/settings.html', context)

def save_settings(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return redirect('/profile/' + request.session.get('user'))
    
# search logic
def search(request):
    active_nav_urls = copy.deepcopy(nav_urls)

    query = request.GET.get('query')
    search_results = [drink for drink in drinks if query.lower() in drink.name.lower() or query.lower() in [i.name for i in drink.ingredients]]
    
    context = {
        'nav_urls': active_nav_urls,
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'mixology/search.html', context)

# follow logic
def follow(request, username):
    if not request.session.get('user'):
        return redirect('/')

    return redirect('/profile/' + username)