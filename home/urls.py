from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/<int:post_id>/<slug:post_slug>/', views.DetailView.as_view(), name='post_detail'),

]