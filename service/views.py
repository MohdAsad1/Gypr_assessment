from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        nationality = request.POST.get('nationality')
        pan_card_number = request.POST.get('pan_card_number')
        gst_number = request.POST.get('gst_number')
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')

        if password != conform_password:
            messages.info(request, "password and confirm password are Not Same")
            return redirect('/signup')

        if first_name == last_name:
            messages.info(request, "First Name and Last Name are Not Same")
            return redirect('/signup')
        try:

            if User.objects.get(first_name=first_name):
                messages.warning(request, "User Name Already Exist")
                return redirect('/signup')
        except Exception as e:
            pass
        try:

            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exist")
                return redirect('/signup')
        except Exception as e:
            pass

        new= User.objects.create(first_name=first_name, last_name=last_name,username=first_name,
                                            email=email,password=password)
        UserProfile.objects.create(user=new,phone_number=phone_number,nationality=nationality,
                                   pan_card_number=pan_card_number,gst_number=gst_number)
        messages.success(request, "User is Created Please Login")
        return redirect('/login')

    return render(request, "signup.html")



def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()

        if user is not None and check_password(password, user.password):
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('/home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')

    return render(request, "login.html")


def handlelogout(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/login')


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})



@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        userprofile= UserProfile.objects.get(user=user)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        nationality = request.POST.get('nationality')
        pan_card_number = request.POST.get('pan_card_number')
        gst_number = request.POST.get('gst_number')
        password = request.POST.get('password')

        # Check if the email is already in use by another user
        if email != user.email and User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already in use by another user")
            return redirect('/edit_profile')

        # Update the user's fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update the user's profile fields
        userprofile.phone_number = phone_number
        userprofile.nationality = nationality
        userprofile.pan_card_number = pan_card_number
        userprofile.gst_number = gst_number
        userprofile.save()

        if password:
            user.set_password(password)
            user.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'edit_profile.html', {'user': user,'user_profile':user_profile})
