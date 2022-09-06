from urllib import response
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse

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
                'posts/main.html', {'posts': serializer.data, 'comment_form': comment_form})

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

# 포스트 좋아요 기능

def post_like(request, post_id):
    response_body = {"result" : ""}
    
    if request.user.is_authenticated:
        if request.method == "POST":

            post = get_object_or_404(models.Post, pk=post_id)
            existed_user = post.image_likes.filter(pk=request.user.id).exists() # image_likes가 있다면 True 없으면 False
            if existed_user:
                # 좋아요 누른 상태일 경우 취소
                post.image_likes.remove(request.user)
                response_body["result"] = "dislike"
                # 좋아요가 아닐 경우 좋아요 표시
            else :
                post.image_likes.add(request.user)
                response_body["result"] = "like"

            return JsonResponse(status=200, data=response_body) # http 상태표 200
    else :
        return JsonResponse(status=403, data=response_body) # http 상태표 403

# 포스트 찾기 기능
def search(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            searchKeyword = request.GET.get("q","")
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                # following된 유저 포스트를 가져온다.
                (Q(author__in=following) | Q(author=user)) & Q(caption__contains=searchKeyword)
            ).order_by('-create_at')
             # .order_by('-created_at') -> 작성일시 순으로 정렬 "-"를 써줌으로 내림차순

            serializer = serializers.PostSerializer(posts, many=True)
            # print(serializer.data)

            return render(
                request,
                'posts/main.html', {'posts': serializer.data, 'comment_form': comment_form})

    else:
        return render(request, 'users/main.html')

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

            return redirect(reverse("posts:index") + "#comment-" + str(comment.id))

        else:
            return render(request, "{% url 'users:login' %}")

# 댓글 삭제 기능
def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comments, pk=comment_id)
        if request.user == comment.author:
            comment.delete()

        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')

# 댓글 수정 기능
def comment_update(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comments, pk=comment_id)
        if request.user != comment.author:
            messages.error('수정권한이 없습니다.')
            return redirect(reverse('post:index'))

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment.contents = form.cleaned_data['contents']
                comment.save()

            return redirect(reverse('posts:index'))
        else :
            form = CommentForm(instance=comment)
        context = {'form': form, 'comment': comment}
        return render(request, 'posts/comment_update.html', context)
    else:
        return render(request, "posts/main.html")
