import copy
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import *

# Create your views here.

nav_urls = [
    {'href': '/', 'name': 'Home', 'active': False, 'icon': 'home.svg'},
    {'href': '/add-drink', 'name': 'New Post', 'active': False, 'icon': 'new-post.svg'},
    {'href': '/profile', 'name': 'Profile', 'active': False, 'icon': 'profile.svg'},
    {'href': '/collections', 'name': 'Collections', 'active': False, 'icon': 'collections.svg'},
    {'href': '/settings', 'name': 'Settings', 'active': False, 'icon': 'settings.svg'},
]

# login/logout
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    if username in users and password == users[username].password:
        request.session['user'] = users[username].username
        request.session['slug'] = users[username].slug
        request.session['role'] = 'admin' if users[username].username == 'admin' else 'user'
        nav_urls[2]['href'] = '/profile/' + users[username].slug
        return redirect('/profile/' + users[username].slug)   
    return redirect('/')
# clear out session vars upon logout
def logout(request):
    request.session.flush()
    return redirect('/')

# home
def index(request):
    feed_drinks = sorted(drinks, key=lambda drink: drink.last_updated, reverse=True)
    # for every view, update the profile link to the user slug
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
    active_nav_urls[0]['active'] = True
    
    context = {
        'feed_drinks': feed_drinks,
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/index.html', context)

# drink logic

def drink(request, slug):
    
    drink = [drink for drink in drinks if drink.slug == slug][0]
    
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')

    context = {
        'nav_urls': active_nav_urls,
        'drink': drink,
    }
    return render(request, 'mixology/drink.html', context)

def add_drink(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
    else :
        return redirect('/')
    active_nav_urls[1]['active'] = True
    
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/add-drink.html', context)

def edit_drink(request, slug):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
    else:
        return redirect('/')
    
    drink = [drink for drink in drinks if drink.slug == slug][0]
    
    context = {
        'nav_urls': active_nav_urls,
        'drink': drink,
    }
    return render(request, 'mixology/edit-drink.html', context)

def delete_drink(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')

    if request.session.get('role') == 'admin' and request.POST.get('submit') == 'delete':
        # TODO: delete drink
        return redirect('/profile/' + request.session.get('slug'))
    else:
        return redirect('/')
    

def save_drink(request):
    # TODO: update drink
    drink = [drink for drink in drinks if drink.slug == request.POST.get('slug')][0]
    req_type = request.POST.get('submit')
    if req_type == 'delete' and request.session.get('role') == 'admin':
        active_nav_urls = copy.deepcopy(nav_urls)
        if request.session.get('user'):
            active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
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
def profile(request, slug):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
    if slug == request.session.get('user'):
        active_nav_urls[2]['active'] = True
    
    user = [v for k, v in users.items() if v.slug == slug][0]
    stats = {
        'followers': len(user.follows),
        'following': len([k for k, v in users.items() if user.slug in v.follows]),
        'drinks': len(user.drinks),
    }
    
    context = {
        'nav_urls': active_nav_urls,
        'viewuser': user,
        'stats': stats,
    }
    return render(request, 'mixology/profile.html', context)

# about
def about(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
        
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/about.html', context)

def contact(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
        
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/contact.html', context)

# collections
def collections(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
    else:
        return redirect('/')
    
    collections = users[request.session.get('user')].collections
    active_nav_urls[3]['active'] = True
    
    context = {
        'nav_urls': active_nav_urls,
        'collections': collections,
    }
    return render(request, 'mixology/collections.html', context)

# settings logic
def settings(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    active_nav_urls[4]['active'] = True
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')
    else:
        return redirect('/')
    
    context = {
        'nav_urls': active_nav_urls,
    }
    return render(request, 'mixology/settings.html', context)

def save_settings(request):
    if not request.session.get('user'):
        return redirect('/')
    
    return redirect('/profile/' + request.session.get('slug'))
    
# search logic
def search(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.session.get('user'):
        active_nav_urls[2]['href'] = '/profile/' + request.session.get('slug')

    query = request.GET.get('query')
    search_results = [drink for drink in drinks if query.lower() in drink.name.lower() or query.lower() in [i.name for i in drink.ingredients]]
    
    context = {
        'nav_urls': active_nav_urls,
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'mixology/search.html', context)

# follow logic
def follow(request, slug):
    if not request.session.get('user'):
        return redirect('/')

    return redirect('/profile/' + slug)