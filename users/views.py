from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()

        return render(request, 'users/signup_.html', {'form':form})

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            
            # 회원가입 후 자동 로그인
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('posts:index'))
        
        return render(request, 'index.html')

def login_views(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect(reverse('posts:index'))
        else:
            return render(request, 'login.html')

def logout_views(request):
    logout(request)
    return redirect('users:index')