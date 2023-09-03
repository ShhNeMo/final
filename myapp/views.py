from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from item.models import *
from .forms import *
import requests

def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'categories': categories,
        'items': items,
    })

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        API = 'o/vyTCZYYIaI395QnNgpeg==VmVz95OtCSESNmC6'
        length = '20'
        api_url = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'.format(length)
        response = requests.get(api_url, headers={'X-Api-Key': API})
        if response.status_code==requests.codes.ok:
            password_rec = response.json()["random_password"]
        else: password_rec = ''

        form = SignupForm()
        return render(request, 'signup.html', {
            'form': form,
            'recommended': password_rec,
        })

@login_required
def profile(request):
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'user_form' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
        elif 'password_form' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()

    return render(request, 'profile.html', {'user_form': user_form, 'password_form': password_form})

def user_logout(request):
    logout(request)
    return redirect('login')

def items_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category, is_sold=False)
    categories = Category.objects.all()

    return render(request, 'index.html', {
        'categories': categories,
        'items': items,
    })
