from django.urls import path
from . import views

app_name = 'mixology'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add-drink/', views.AddDrinkView.as_view(), name='add-drink'),
    path('profile/<slug:slug>', views.ProfileView.as_view(), name='profile'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('collections/', views.CollectionsView.as_view(), name='collections'),
    path('drink/<slug:slug>/', views.DrinkView.as_view(), name='drink'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('search/<str:query>/', views.SearchView.as_view(), name='search'),
]