from collections import Counter
import copy
import json
from django.utils import timezone
from django.contrib import messages, auth
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from actions.models import Action
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.

nav_urls = [
    {'href': '/', 'name': 'Home', 'active': False, 'icon': 'home.svg'},
    {'href': '/add-drink', 'name': 'New Post', 'active': False, 'icon': 'new-post.svg'},
    {'href': '/profile', 'name': 'Profile', 'active': False, 'icon': 'profile.svg'},
    {'href': '/collections', 'name': 'Collections', 'active': False, 'icon': 'collections.svg'},
    {'href': '/settings', 'name': 'Settings', 'active': False, 'icon': 'settings.svg'},
]

def get_nav_urls(request):
    active_nav_urls = copy.deepcopy(nav_urls)
    if request.user.is_authenticated:
        active_nav_urls[2]['href'] = '/profile/' + request.user.username
        active_nav_urls[3]['href'] = '/collections/' + request.user.username
        active_nav_urls[4]['href'] = '/settings/' + str(request.user.profile.id)
    return active_nav_urls

# Get user activity
def get_user_activity(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'GET' and is_ajax:
        uid = request.GET.get('uid')
        user_only = request.GET.get('user_only')
        try:
            user = User.objects.get(pk=uid)
            # user Q object to filter actions : https://docs.djangoproject.com/en/5.1/topics/db/queries/#complex-lookups-with-q-objects 
            if user_only == 'true':
                actions = Action.objects.filter(actor=user.profile).order_by('-timestamp')
            elif user_only == 'false':
                following_users = user.profile.get_following().all()
                actions = Action.objects.filter(
                    Q(actor__in=following_users) | Q(actor=user.profile)
                ).order_by('-timestamp')
            action_list = []
            for action in actions:
                action_dict = {
                    'action_type': action.Types.get_verb(action.action_type),
                    'timestamp': action.get_human_readable_time(),
                    'target': action.target.getJSON() if action.target else None,
                    'user': action.actor.getJSON(),
                }
                action_list.append(action_dict)

            return JsonResponse({'success': True, 'actions': action_list, 'username': user.username}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

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
        firstname = request.POST.get('first-name')
        lastname = request.POST.get('last-name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
        
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
        active_nav_urls = get_nav_urls(self.request)
        active_nav_urls[0]['active'] = True
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
        active_nav_urls = get_nav_urls(self.request)
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
        active_nav_urls = get_nav_urls(self.request)
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
        
        drink.ingredients.clear()

        ingredient_names = self.request.POST.getlist('ingredients[]')
        for name in ingredient_names:
            name = name.strip().lower()
            if name:
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                drink.ingredients.add(ingredient)
        response = super().form_valid(form)
        
        # log action
        action = Action(actor=self.request.user.profile, action_type=Action.Types.EDIT, target=drink)
        action.save()
        messages.info(self.request, 'Drink updated successfully!')
        return response

class AddDrinkView(generic.CreateView):
    model = Drink
    template_name = 'mixology/add-drink.html'
    fields = ['name', 'description', 'instructions', 'ingredients', 'image']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = get_nav_urls(self.request)
        context['nav_urls'] = active_nav_urls
        return context
    
    def form_valid(self, form):
        drink = form.instance
        drink.poster = self.request.user.profile
        drink.last_updated = timezone.now()
        drink.status = Drink.Status.PUBLISHED
        image = self.request.FILES['image']
        if image:
            drink.image = image
        response = super().form_valid(form)

        ingredient_names = self.request.POST.getlist('ingredients[]')
        for name in ingredient_names:
            name = name.strip().lower()
            if name:
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                drink.ingredients.add(ingredient)
        # log the action
        action = Action(actor=self.request.user.profile, action_type=Action.Types.POST, target=drink)
        action.save()
        
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
        active_nav_urls = get_nav_urls(self.request)
        active_nav_urls[2]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            messages.error(self.request, 'User not found.')
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
        active_nav_urls = get_nav_urls(self.request)
        active_nav_urls[3]['active'] = True
        context['nav_urls'] = active_nav_urls
        username = self.kwargs.get('username')
        try:
            context['owner'] = User.objects.get(username=username)
        except User.DoesNotExist:
            context['owner'] = None
            messages.error(self.request, 'User not found.')
        return context
    
    def get_queryset(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
            collections = user.profile.collections.all()
            if collections.exists():
                return collections
            else:
                return []
        except User.DoesNotExist:
            messages.error(self.request, 'User not found.')
            return []
        
class CollectionDetailView(generic.DetailView):
    model = Collection
    template_name = 'mixology/collection.html'
    context_object_name = 'collection'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = get_nav_urls(self.request)
        active_nav_urls[3]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        cid = self.kwargs.get('cid')
        return get_object_or_404(Collection, pk=cid)
    
def create_collection(request):
    if request.method == 'POST':
        name = request.POST.get('collection-name')
        Collection.objects.create(name=name, owner=request.user.profile)
        messages.success(request, 'Collection created successfully!')
        return redirect('mixology:collections', username=request.user.username)
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('mixology:home')
    
def save_drink_to_collections(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        uid = request.POST.get('uid')
        did = request.POST.get('did')
        cid_map = request.POST.get('collections')
        cid_map = json.loads(cid_map)
        try:
            user = User.objects.get(pk=uid)
            drink = Drink.objects.get(pk=did)
            for cid, is_checked in cid_map.items():
                collection = Collection.objects.get(pk=cid)
                if collection.owner != user.profile:
                    return JsonResponse({'error': 'You do not own this collection'}, status=200)
                if is_checked and not collection.drinks.filter(pk=drink.id).exists():
                    collection.drinks.add(drink)
                elif not is_checked and collection.drinks.filter(pk=drink.id).exists():
                    collection.drinks.remove(drink)
            collection.save()
            # log action
            action = Action(actor=request.user.profile, action_type=Action.Types.SAVE, target=drink)
            action.save()
            return JsonResponse({'success': True}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
        except Drink.DoesNotExist:
            return JsonResponse({'error': 'Drink not found'}, status=200)
        except Collection.DoesNotExist:
            return JsonResponse({'error': 'Collection not found'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=200)
        
def get_user_collections(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'GET' and is_ajax:
        uid = request.GET.get('uid')
        did = request.GET.get('did')
        try:
            user = User.objects.get(pk=uid)
            collections = user.profile.collections.all()
            collection_list = []
            for collection in collections:
                collection_list.append({
                    'id': collection.id,
                    'name': collection.name,
                    'drink_exists': collection.drinks.filter(pk=did).exists(),
                })
            return JsonResponse({'success': True, 'collections': collection_list, 'username': user.username}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=200)
        
def delete_collection(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        cid = request.POST.get('cid')
        try:
            collection = Collection.objects.get(pk=cid)
            collection.delete()
            return JsonResponse({'success': True}, status=200)
        except Collection.DoesNotExist:
            return JsonResponse({'error': 'Collection not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_drink_from_collection(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        cid = request.POST.get('cid')
        did = request.POST.get('did')
        try:
            collection = Collection.objects.get(pk=cid)
            drink = Drink.objects.get(pk=did)
            collection.drinks.remove(drink)
            return JsonResponse({'success': True}, status=200)
        except Collection.DoesNotExist:
            return JsonResponse({'error': 'Collection not found'}, status=200)
        except Drink.DoesNotExist:
            return JsonResponse({'error': 'Drink not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

# settings logic
class SettingsView(generic.UpdateView):
    model = UserProfile
    template_name = 'mixology/settings.html'
    fields = ['bio', 'pfp']
    context_object_name = 'user_profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_nav_urls = get_nav_urls(self.request)
        active_nav_urls[4]['active'] = True
        context['nav_urls'] = active_nav_urls
        return context
    
    def get_object(self):
        return get_object_or_404(UserProfile, pk=self.kwargs.get('uid'))
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and self.request.user.profile.id != self.kwargs.get('uid'):
            return redirect('mixology:home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user_profile = form.instance
        
        current_password = self.request.POST.get('current-password')
        new_password = self.request.POST.get('new-password')
        confirm_password = self.request.POST.get('confirm-password')
        
        if new_password and confirm_password:
            # check if current password is correct
            if self.request.user.id == user_profile.user.id and not current_password:
                messages.error(self.request, 'Current password is required to change password.')
                return self.form_invalid(form)
            if new_password == user_profile.user.password:
                messages.error(self.request, 'New password cannot be the same as current password.')
                return self.form_invalid(form)
            elif new_password == confirm_password:
                if self.request.user.id == user_profile.user.id:
                    if self.request.user.check_password(current_password):
                        self.request.user.set_password(new_password)
                        self.request.user.save()
                        auth.update_session_auth_hash(self.request, self.request.user)
                        
                        messages.success(self.request, 'Password updated successfully!')
                    else:
                        messages.error(self.request, 'Current password is incorrect.')
                        return self.form_invalid(form)
                else:
                    self.request.user.set_password(new_password)
                    self.request.user.save()
                    messages.success(self.request, 'Password updated successfully!')
                    
            else:
                messages.error(self.request, 'New passwords do not match.')
                return self.form_invalid(form)
                
        user_profile.user.first_name = self.request.POST.get('first-name')
        user_profile.user.last_name = self.request.POST.get('last-name')
        user_profile.user.email = self.request.POST.get('email')
        
        role = self.request.POST.get('role')
        if role == 'admin':
            user_profile.user.is_staff = True
            user_profile.user.is_superuser = True
        elif role == 'user':
            user_profile.user.is_staff = False
            user_profile.user.is_superuser = False
        
        user_profile.user.save()
        image = self.request.FILES.get('pfp')
        if image:
            user_profile.pfp = image
            
        response = super().form_valid(form)
        
        messages.info(self.request, 'Profile updated successfully!')
        return response
    
    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)


# search logic
def search(request):
    active_nav_urls = get_nav_urls(request)

    query = request.GET.get('query')
    
    search_results = []
    
    if query:
        user_results = User.objects.filter(username__icontains=query)
        name_results = list(Drink.objects.filter(name__icontains=query, status=Drink.Status.PUBLISHED))
        ingredient_results = list(Drink.objects.filter(ingredients__name__icontains=query, status=Drink.Status.PUBLISHED))

        all_results = {drink.id: drink for drink in name_results + ingredient_results}

        search_results = sorted(all_results.values(), key=lambda d: d.last_updated, reverse=True)

        if not search_results and not user_results:
            messages.warning(request, f'No results found for "{query}"')
        else:
            messages.success(request, f'Found {len(search_results) + len(user_results) + len(ingredient_results)} results for "{query}"')
    else:
        messages.error(request, 'Please enter a search term.')
        return redirect('mixology:home')
    
    context = {
        'nav_urls': active_nav_urls,
        'query': query,
        'user_results': user_results,
        'post_results': search_results,
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
            follow_count = user.profile.get_followers().count()
            
            if is_following:
                request.user.profile.follows.remove(user.profile)
                follow_count -= 1
                is_following = False
            else:
                request.user.profile.follows.add(user.profile)
                follow_count += 1
                is_following = True
                # log action
                action = Action(actor=request.user.profile, action_type=Action.Types.FOLLOW, target=user.profile)
                action.save()
                
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
            # log action
            action = Action(actor=request.user.profile, action_type=Action.Types.COMMENT, target=comment_obj)
            action.save()
            return JsonResponse({'success': True, 'comment': comment, 'posted': comment_obj.posted, 'username': comment_obj.user.username, 'pfp_url':comment_obj.user.profile.get_pfp_url(), "cid": comment_obj.id}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=200)
        except Drink.DoesNotExist:
            return JsonResponse({'error': 'Drink not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def delete_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        cid = request.POST.get('cid')
        try:
            comment = Comment.objects.get(pk=cid)
            drink_id = comment.drink.id
            comment.delete()
            return JsonResponse({'success': True, 'drink_id': drink_id}, status=200)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def edit_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        cid = request.POST.get('cid')
        comment_text = request.POST.get('comment')
        try:
            comment = Comment.objects.get(pk=cid)
            drink_id = comment.drink.id
            comment.text = comment_text
            comment.posted = timezone.now()
            comment.save()
            return JsonResponse({'success': True, 'drink_id': drink_id, 'comment': comment_text}, status=200)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    