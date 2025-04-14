from django.urls import path
from . import views

app_name = 'mixology'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('add-drink/', views.AddDrinkView.as_view(), name='add-drink'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('profile-order/', views.profile_order, name="profile-order"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('collections/', views.CollectionView.as_view(), name='collections'),
    path('drink/<int:did>/', views.DrinkView.as_view(), name='drink'),
    path('comment/', views.comment, name='comment-drink'),
    path('edit-drink/<int:did>/', views.EditDrinkView.as_view(), name='edit-drink'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('search/', views.search, name='search'),
    path('follow/', views.follow, name='follow-user'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('process-signup/', views.process_signup, name='process-signup'),
    path('process-login/', views.process_login , name='login'),
    path('logout/', views.logout, name='logout'),
]