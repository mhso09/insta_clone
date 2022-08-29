from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime

from .forms import CreatePostForm, CommentForm, UpdatePostForm
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
            ).order_by('-create_at') # .order_by('-created_at') -> 작성일시 순으로 정렬 "-"를 써줌으로 내림차순

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

            return redirect(reverse('posts:index'))

        else :
            return render(request, "index.html")

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

            return redirect(reverse("posts:main") + "#comment-" + str(comment.id))

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

# 포스트 수정 기능

def post_update(request, post_id):
    # post = get_object_or_404(models.Post, pk=post_id)
    # if request.method == 'POST':
    #     form = CreatePostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.updated_at = datetime.now()
    #         post.save()
    #         return redirect(reverse("posts:index", post_id=post.id))
    # else:
    #     form = CreatePostForm(instance=post)
    # context = {"form" : form}
    # return render(request, "posts/post_update.html", context)

    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user != post.author:
            messages.error('수정권한이 없습니다.')
            return redirect(reverse('post:index'))

        if request.method == 'GET':
            form = UpdatePostForm(instance=post)
            return render(
                request,
                'posts/post_update.html',
                {'form': form, 'post': post}
                )

        elif request.method == 'POST':
            form = UpdatePostForm(request.POST)
            if form.is_valid():
                post.caption = form.cleaned_data['caption']
                post.save()

            return redirect(reverse('posts:index'))

    else:
        return render(request, "posts/main.html")
