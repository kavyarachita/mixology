from django.urls import path
from . import views

app_name = 'mixology'

urlpatterns = [
    path('', views.index, name='home'),
    path('add-drink/', views.add_drink, name='add-drink'),
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('collections/', views.collections, name='collections'),
    path('drink/<slug:slug>/', views.drink, name='drink'),
    path('edit-drink/<slug:slug>/', views.edit_drink, name='edit-drink'),
    path('save-drink/', views.save_drink, name='save-drink'),
    path('delete-drink/', views.delete_drink, name='delete-drink'),
    path('settings/', views.settings, name='settings'),
    path('save-settings/', views.save_settings, name='save-settings'),
    path('search/', views.search, name='search'),
    path('follow/<slug:slug>/', views.follow, name='follow'),
    path('login/', views.login , name='login'),
    path('logout/', views.logout, name='logout'),
]