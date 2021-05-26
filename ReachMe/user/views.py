from django.db.models.deletion import SET_DEFAULT
import user
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import FriendShipStatus, UserInfo
from .utils import get_friends, get_incoming_requests, get_recommendations
from .forms import CreateUserForm, CreateUserInfoForm


@login_required(login_url='login')
def homePage(request):
    """User will see recommendations of other users here"""
    if request.method == 'POST' and 'send_request' in request.POST:
        print(f"Sent friend request to {request.POST.get('requested_user')}")
        requested_user = str(request.POST.get('requested_user'))

        if request.user != requested_user:
            user_a = User.objects.get(username=request.user)
            user_b = User.objects.get(username=requested_user)

            if str(request.user) < requested_user:
                if FriendShipStatus.objects.filter(status='ab').filter(user_a=user_a).filter(user_b=user_b).first() is None:
                    req = FriendShipStatus(user_a=user_a, user_b=user_b, status='ab')
                    req.save()
            else:
                if FriendShipStatus.objects.filter(status='ba').filter(user_a=user_b).filter(user_b=user_a).first() is None:
                    req = FriendShipStatus(user_a=user_b, user_b=user_a, status='ba')
                    req.save()
    recommendations = get_recommendations(request.user)
    context = {
        "recommendations": recommendations,
        "user_id": request.user
    }
    return render(request, 'user/home.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, 'Account was created for ' + username)
            return redirect('settings')

    context = {'form': form}
    return render(request, 'user/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboardPage(request, user_id):
    return render(request, 'user/dashboard.html', context={
        'user': UserInfo.objects.filter(user=user_id).first()
    })


@login_required(login_url='login')
def settingsPage(request):
    form = CreateUserInfoForm(initial={'user': request.user})

    if request.method == 'POST':
        form = CreateUserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['user'] = request.user
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'user/settings.html', context)

@login_required(login_url='login')
def friendsPage(request):
    if request.method == 'POST':
        requested_user = str(request.POST.get('requested_user'))
        if request.user != requested_user:
            user_a = User.objects.get(username=request.user)
            user_b = User.objects.get(username=requested_user)

            if str(request.user) < requested_user:
                FriendShipStatus.objects.filter(status='axb').filter(user_a=user_a).filter(user_b=user_b).delete()
            else:
                FriendShipStatus.objects.filter(status='axb').filter(user_a=user_b).filter(user_b=user_a).delete()

    context = {
        'friends': get_friends(request.user),
        'user_id': request.user
    }
    return render(request, 'user/friends.html', context)

@login_required(login_url='login')
def incomingRequestsPage(request):
    if request.method == 'POST':
        requested_user = str(request.POST.get('requested_user'))
        if request.user != requested_user:
            user_a = User.objects.get(username=request.user)
            user_b = User.objects.get(username=requested_user)

            if str(request.user) < requested_user:
                FriendShipStatus.objects.filter(status='ba').filter(user_a=user_a).filter(user_b=user_b).delete()
                if 'accept_request' in request.POST:
                    req = FriendShipStatus(user_a=user_a, user_b=user_b, status='axb')
                    req.save()
            else:
                FriendShipStatus.objects.filter(status='ab').filter(user_a=user_b).filter(user_b=user_a).delete()
                if 'accept_request' in request.POST:
                    req = FriendShipStatus(user_a=user_b, user_b=user_a, status='axb')
                    req.save()
    context = {
        'incoming_requests': get_incoming_requests(request.user),
        'user_id': request.user
    }
    return render(request, 'user/incoming_requests.html', context)