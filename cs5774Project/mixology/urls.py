from django.urls import path
from . import views

app_name = 'mixology'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('get-user-activity/', views.get_user_activity, name='get-user-activity'),
    path('add-drink/', views.AddDrinkView.as_view(), name='add-drink'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('collections/<str:username>', views.CollectionView.as_view(), name='collections'),
    path('collection/<int:cid>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    path('create-collection/', views.create_collection, name='create-collection'),
    path('get-collections/', views.get_user_collections, name='get-collections'),
    path('save-drink-to-collections/', views.save_drink_to_collections, name='save-drink-to-collections'),
    path('delete-drink-from-collection/', views.delete_drink_from_collection, name='delete-drink-from-collection'),
    path('delete-collection/', views.delete_collection, name='delete-collection'),
    path('drink/<int:did>/', views.DrinkView.as_view(), name='drink'),
    path('comment/', views.comment, name='comment-drink'),
    path('delete-comment/', views.delete_comment, name='delete-comment'),
    path('edit-comment/', views.edit_comment, name='edit-comment'),
    path('edit-drink/<int:did>/', views.EditDrinkView.as_view(), name='edit-drink'),
    path('settings/<int:uid>', views.SettingsView.as_view(), name='settings'),
    path('search/', views.search, name='search'),
    path('follow/', views.follow, name='follow-user'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('process-signup/', views.process_signup, name='process-signup'),
    path('process-login/', views.process_login , name='login'),
    path('logout/', views.logout, name='logout'),
]