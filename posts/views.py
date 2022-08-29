from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import CreatePostForm, CommentForm
from users.models import User as user_model
from . import models, serializers
# Create your views here.

def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                Q(author__in=following) | Q(author=user) #following된 유저 포스트를 가져온다.
            )

            serializer = serializers.PostSerializer(posts, many=True)
            # print(serializer.data)

            return render(
                request, 
                'posts/main.html', 
                {'posts': serializer.data, 'comment_form':comment_form})

# 포스트 작성 기능
def post_create(request):
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {'form' : form})

    elif request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            #     )
            # new_post.save()

            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else :
                print(form.errors)

            return render (request, 'posts/main.html')

        else :
            return render (request, 'index.html')

# 댓글 작성 기능
def comment_create(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.save()

            return redirect(reverse('posts:index') + "#comment-" + str(comment.id))

        else:
            return render(request, "{% url 'users:login' %}")

# 댓글 삭제 기능
def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comments, pk=comment_id)
        if request.user == comment.author:
            comment.delete()

        return redirect(reverse('posts:index'))

    else :
        return render(request, 'users/main.html')

# 포스트 삭제 기능
def post_delete(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user == post.author:
            post.delete()
        
        return redirect(reverse('posts:index'))
    
    else :
        return render(request, 'users/main.html')