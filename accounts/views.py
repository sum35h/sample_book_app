from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',{'error':'Username already exists.'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html',{'error':'Passwords Dont Match!'})
   
    else:
         return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        print('post=============')
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user !=None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error':'Username or Password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
        
