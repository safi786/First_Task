from django.urls import path
# now import the views.py file into this code
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('forget_password/', views.forget_password, name="forget_password"),
    path('dashboard/', views.index, name="dashboard"),
    path('logout/', views.logoutUser, name="logout"),
]