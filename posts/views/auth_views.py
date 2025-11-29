from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse


# Normal user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('/')  # redirect normal user home
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

# Staff login
def staff_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/staff/')  # redirect to staff dashboard
        else:
            messages.error(request, "Invalid staff credentials")
    return render(request, 'staff_login.html')


def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
    # return redirect('/')  




def login_or_create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        # User exists → try to authenticate
        if user:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(request.META.get("HTTP_REFERER", "home"))
                # return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
                return redirect(request.META.get("HTTP_REFERER", "home"))

        # User does not exist → create new user
        new_user = User.objects.create_user(username=username, password=password)
        login(request, new_user)
        return redirect(request.META.get("HTTP_REFERER", "home"))
        # return redirect('home')

    messages.error(request, "Invalid request")
    return redirect('home')


def login_or_create_user_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"status": "success", "message": "Logged in"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid credentials"})
        else:
            # Create new user
            new_user = User.objects.create_user(username=username, password=password)
            new_user.is_staff = False
            new_user.save()
            login(request, new_user)
            return redirect('home')
            # return JsonResponse({"status": "success", "message": "User created and logged in"})

    return JsonResponse({"status": "error", "message": "Invalid request"})