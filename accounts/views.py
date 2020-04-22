from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('community:review_list')
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user=form.save()
                authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
                auth_login(request,authenticated_user)
                return redirect('community:review_list')
        else:
            form = UserCreationForm()
        context = {
            'form':form
        }
        return render(request, 'accounts/signup.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('community:review_list')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request,request.POST) #
            if form.is_valid():
                auth_login(request,form.get_user()) # AuthenticationForm 메서드
                return redirect(request.GET.get('next') or 'community:review_list') #
        else:
            form = AuthenticationForm()
        context={
            'form':form
        }
        return render(request,'accounts/login.html',context)

@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('community:review_list')