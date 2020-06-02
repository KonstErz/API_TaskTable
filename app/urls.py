from django.urls import path
from .views import (RegistrationView, LoginView, LogoutView, TaskCreationView,
                    CommentAddingView)


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('taskcreation/', TaskCreationView.as_view()),
    path('addcomment/', CommentAddingView.as_view()),
]
