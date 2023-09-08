from django.urls import path
from service import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.handlelogin, name="login"),
    path('logout/', views.handlelogout, name="handlelogout"),
    path('profile', views.profile, name="profile"),
    path('edit_profile', views.edit_profile, name='edit_profile'),

]