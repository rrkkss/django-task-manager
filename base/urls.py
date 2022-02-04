from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('profile/<int:pk>', views.userProfile, name="user-profile"),

    path('profile/add/<int:pk>', views.addTask, name="add-task"),
    path('profile/update/<int:pk>', views.updateTask, name="update-task"),
    path('profile/remove/<int:pk>', views.removeTask, name="remove-task"),

    #path('error', views.renderError, name="error"),
]
