from django.urls import path
from .views import main_post_view, liked_unliked_view, PostDeleteView, PostUpdateView

app_name = 'posts'

urlpatterns = [
    path('',main_post_view, name='main-post-view'),
    path('liked/',liked_unliked_view, name='liked-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
]