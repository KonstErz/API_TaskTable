from django.urls import path, include
from .views import (RegistrationView, LoginView, LogoutView, TaskCreationView,
                    CommentAddingView, TaskViewSet)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('taskcreation/', TaskCreationView.as_view()),
    path('addcomment/', CommentAddingView.as_view()),
    path('', include(router.urls)),
]
