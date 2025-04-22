import copy
from django.utils import timezone
from django.contrib import messages, auth
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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

def login(request):
    context = {
        'nav_urls': nav_urls,
    }
    return render(request, 'mixology/login.html', context)

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
        
        # Log the user in
        auth.login(request, user)
        request.session['user'] = username
        return redirect('/')
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
        context['filter'] = self.request.GET.get('filter', 'all')
        return context

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', 'all')
        drinks = Drink.objects.filter(status=Drink.Status.PUBLISHED)
        
        if filter_val == 'following' and self.request.user.is_authenticated:
            following_users = self.request.user.profile.get_following().all()
            drinks = drinks.filter(poster__in=following_users)

        return drinks.order_by('-last_updated')

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
        context['comments'] = self.object.comments.all()
        return context
    
    def get_object(self):
        drink_id = self.kwargs.get('did')
        return Drink.objects.get(pk=drink_id)

class EditDrinkView(generic.UpdateView):
    model = Drink
    template_name = 'mixology/edit-drink.html'
    fields = ['name', 'description', 'instructions', 'ingredients', 'image']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        return get_object_or_404(Drink, pk=self.kwargs.get('did'))
    
    def form_valid(self, form):
        submit_type = self.request.POST.get('submit', 'save')
        # Handle the delete action
        if submit_type == 'delete':
            drink = self.get_object()
            drink.delete()
            messages.warning(self.request, 'Drink deleted successfully!')
            return redirect('mixology:home') 
        
        drink = form.instance
        drink.last_updated = timezone.now()
        image = self.request.FILES.get('image')
        if image:
            drink.image = image
        response = super().form_valid(form)
        drink.ingredients.clear()

        ingredient_names = self.request.POST.getlist('ingredients[]')
        for name in ingredient_names:
            name = name.strip().lower()
            if name:
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                drink.ingredients.add(ingredient)

        messages.info(self.request, 'Drink updated successfully!')
        return response

class AddDrinkView(generic.CreateView):
    model = Drink
    template_name = 'mixology/add-drink.html'
    fields = ['name', 'description', 'instructions', 'ingredients', 'image']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def form_valid(self, form):
        print(f"Form data: {self.request.POST}")
        drink = form.instance
        drink.poster = self.request.user.profile
        drink.last_updated = timezone.now()
        drink.status = Drink.Status.PUBLISHED
        image = self.request.FILES['image']
        if image:
            drink.image = image
        response = super().form_valid(form)

        ingredient_names = self.request.POST.getlist('ingredients[]')
        print(ingredient_names)
        for name in ingredient_names:
            name = name.strip().lower()
            if name:
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                drink.ingredients.add(ingredient)
                print(f"Added ingredient: {ingredient.name}")

        messages.success(self.request, 'Drink added successfully!')
        return response
    
    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)  # This will show you exactly what failed
        return super().form_invalid(form)


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
            active_nav_urls[2]['href'] = '/s.' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return UserProfile.objects.get(user__username=username)
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
        collections = self.request.user.profile.collections.all()
        return collections

# settings logic
class SettingsView(generic.UpdateView):
    model = UserProfile
    template_name = 'mixology/settings.html'
    fields = ['name', 'bio', 'pfp']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = copy.deepcopy(nav_urls)
        active_nav_urls[4]['active'] = True
        if self.request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + self.request.user.username
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def form_valid(self, form):
        print(f"Form data: {self.request.POST}")
        user_profile = form.instance
        image = self.request.FILES.get('pfp')
        if image:
            user_profile.pfp = image
        response = super().form_valid(form)
        
        messages.info(self.request, 'Profile updated successfully!')
        return response


# search logic
def search(request):
    active_nav_urls = copy.deepcopy(nav_urls)

    query = request.GET.get('query')
    
    search_results = []
    
    if query:
        name_results = list(Drink.objects.filter(name__icontains=query, status=Drink.Status.PUBLISHED))
        ingredient_results = list(Drink.objects.filter(ingredients__name__icontains=query, status=Drink.Status.PUBLISHED))

        all_results = {drink.id: drink for drink in name_results + ingredient_results}

        search_results = sorted(all_results.values(), key=lambda d: d.last_updated, reverse=True)

        if not search_results:
            messages.warning(request, f'No results found for "{query}"')
        else:
            messages.success(request, f'Found {len(search_results)} results for "{query}"')
    else:
        messages.error(request, 'Please enter a search term.')
        return redirect('mixology:home')
    
    if request.user.is_authenticated:
            active_nav_urls[2]['href'] = '/profile/' + request.user.username
    
    context = {
        'nav_urls': active_nav_urls,
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'mixology/search.html', context)

# follow logic
def follow(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        uid = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=uid)
            is_following = request.user.profile.follows.filter(pk=uid).exists()
            follow_count = request.user.profile.follows.count()
            if is_following:
                request.user.profile.follows.remove(user.profile)
                follow_count -= 1
                is_following = False
            else:
                request.user.profile.follows.add(user.profile)
                follow_count += 1
                is_following = True
            request.user.profile.save()
            return JsonResponse({'success': True, 'follower_count': follow_count, 'is_following': is_following}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        uid = request.POST.get('user_id')
        did = request.POST.get('drink_id')
        comment = request.POST.get('comment')
        try:
            comment_obj = Comment(text=comment)
            comment_obj.drink = Drink.objects.get(pk=did)
            comment_obj.user = User.objects.get(pk=uid)
            comment_obj.posted = timezone.now()
            comment_obj.save()
           
            return JsonResponse({'success': True, 'comment': comment, 'posted': comment_obj.posted, 'username': comment_obj.user.username, 'pfp_url':comment_obj.user.profile.get_pfp_url()}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
        except Drink.DoesNotExist:
            return JsonResponse({'error': 'Drink not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def profile_order(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'GET' and is_ajax:
        uid = request.GET.get('uid')
        filter = request.GET.get('filter')
        try:
            user = User.objects.get(pk=uid)
            drinks = user.profile.drinks.all()
            if filter == 'all':
                drinks = drinks.order_by('-id')
            elif filter == 'recent':
                drinks = drinks.order_by('-last_updated')
            elif filter == 'oldest':
                drinks = drinks.order_by('last_updated')
            drink_data = []
            for drink in drinks:
                drink_data.append({
                    'id': drink.id,
                    'name': drink.name,
                    'image_url': drink.get_image_url(),
                    'last_updated': drink.last_updated,
                })
            return JsonResponse({'success': True, 'drinks': drink_data}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)