from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    #path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('signup/', views.newSignupView, name='account_signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
]