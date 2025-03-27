import copy
from django.shortcuts import render
from django.http import HttpResponse
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

class SearchView(generic.ListView):
    model = Drink
    template_name = 'mixology/search.html'
    context_object_name = 'search_results'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_urls'] = nav_urls
        return context
    
    def get_queryset(self):
        return Drink.objects.filter(name__icontains=self.kwargs['query'])
    
class IndexView(generic.ListView):
    model = Drink
    template_name = 'mixology/index.html'
    context_object_name = 'feed_drinks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[0]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_queryset(self):
        return Drink.objects.order_by('-last_updated')[:5]
    
class AddDrinkView(generic.TemplateView):
    template_name = 'mixology/add-drink.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[1]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context

class ProfileView(generic.DetailView):
    model = User
    template_name = 'mixology/profile.html'
    context_object_name = 'viewuser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        if self.kwargs['slug'] == 'me':
            active_nav_urls[2]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context

class AboutView(generic.TemplateView):
    template_name = 'mixology/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_urls'] = nav_urls
        return context

class ContactView(generic.TemplateView):
    template_name = 'mixology/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_urls'] = nav_urls
        return context

class CollectionsView(generic.TemplateView):
    template_name = 'mixology/collections.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[3]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context

class DrinkView(generic.DetailView):
    model = Drink
    template_name = 'mixology/drink.html'
    context_object_name = 'drink'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_urls'] = nav_urls
        return context

class SettingsView(generic.TemplateView):
    template_name = 'mixology/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[4]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context
