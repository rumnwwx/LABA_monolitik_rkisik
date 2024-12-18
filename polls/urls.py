from django.urls import path

from . import views
from .views import custom_logout, ProfileUpdate

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', views.UserProfileListView.as_view(), name='profile'),
    path('update/', ProfileUpdate.as_view(), name='profile_update'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.question_list, name='question_list'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
]