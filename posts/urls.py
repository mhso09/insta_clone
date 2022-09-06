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
    path('<int:post_id>/post_update/', views.post_update, name='post_update'),

    #/posts/1/post_like/
    path('<int:post_id>/post_like/', views.post_like, name='post_like'),
    
    # /posts/search/
    path('search/', views.search, name='post_search'),

# 댓글 기능

    # /posts/1/comment_create/
    path('<int:post_id>/comment_create/', views.comment_create, name='comment_create'),
    
    # /posts/1/comment_delete/
    path('<int:comment_id>/comment_delete/',
         views.comment_delete, name='comment_delete'),

    # /posts/1/comment_update/
    path('<int:comment_id>/comment_update/',
         views.comment_update, name='comment_update'),
]
