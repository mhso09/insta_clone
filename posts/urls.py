from django.urls import path
from . import views
app_name = 'posts'

urlpatterns = [
    #  # /posts/
    path('', views.index, name='index'),

# 포스트 기능

    # /posts/create/
    path('create/', views.post_create, name='post_create'),

    # /posts/1/post_delete/
    path('<int:post_id>/post_delete/', views.post_delete, name='post_delete'),

    # /posts/1/post_update/

# 댓글 기능

    # /posts/1/comment_create/
    path('<int:post_id>/comment_create/', views.comment_create, name='comment_create'),
    
    # /posts/1/comment_delete/
    path('<int:comment_id>/comment_delete/',
         views.comment_delete, name='comment_delete'),

    # /posts/1/comment_update/
]
