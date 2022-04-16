from django.urls import path
# now import the views.py file into this code
from . import views

urlpatterns = [
    path('', views.user_login, name="login"),
    path('register/', views.signup, name="register"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('forget_password/', views.forget_password, name="forget_password"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/', views.profile, name="profile"),
    path('deleteExchange/<int:pk>/delete/', views.deleteExchange.as_view(), name="deleteExchange"),
    path('deleteAsset/<int:pk>/delete/', views.deleteAsset.as_view(), name="deleteAsset"),
    path('updatePassword/', views.updatePassword, name="updatePassword"),
    path('logout/', views.logoutUser, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset")
]
