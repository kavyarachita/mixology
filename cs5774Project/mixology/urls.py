from django.urls import path
from . import views

app_name = 'mixology'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('add-drink/', views.add_drink, name='add-drink'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('collections/', views.CollectionView.as_view(), name='collections'),
    path('drink/<int:did>/', views.DrinkView.as_view(), name='drink'),
    path('edit-drink/<int:did>/', views.edit_drink, name='edit-drink'),
    path('save-drink/', views.save_drink, name='save-drink'),
    path('delete-drink/', views.delete_drink, name='delete-drink'),
    path('settings/', views.settings, name='settings'),
    path('save-settings/', views.save_settings, name='save-settings'),
    path('search/', views.search, name='search'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('signup/', views.signup, name='signup'),
    path('process-signup/', views.process_signup, name='process-signup'),
    path('login/', views.process_login , name='login'),
    path('logout/', views.logout, name='logout'),
]