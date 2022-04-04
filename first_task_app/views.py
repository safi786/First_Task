from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    user = authenticate(request, username=user.username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        messages.info(request, 'Username OR password is incorrect')
                else:
                    messages.info(request, 'Username OR password is incorrect')
            except:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account has been created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)




def dashboard(request):
    userForm = UserForm(instance=request.user)
    profileForm = ProfileForm(instance=request.user.profile)
    userExchangeInstance = UserExchange.objects.get(user=request.user)
    exchangeForm = UserExchangeForm(instance=userExchangeInstance)
    context = {'userForm': userForm, 'profileForm': profileForm, 'exchangeForm': exchangeForm}
    return render(request, 'dashboard.html', context)


def profile(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=request.user)
        profileForm = ProfileForm(request.POST, instance=request.user.profile)
        userExchangeInstance = UserExchange.objects.get(user=request.user)
        exchangeForm = UserExchangeForm(request.POST, instance=userExchangeInstance)
        if userForm.is_valid() and profileForm.is_valid():
            print('userform is valid')
            userForm.save()
            profileForm.save()
            messages.success(request, ('Your profile was successfully updated!'))
        else:
            messages.error(request, ('Please correct the error below.'))
        if exchangeForm.is_valid():
            exchangeForm.save()
        return redirect('profile')

    else:
        userForm = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=request.user.profile)
        userExchangeInstance = UserExchange.objects.get(user=request.user)
        exchangeForm = UserExchangeForm(instance=userExchangeInstance)
        context = {'userForm': userForm, 'profileForm': profileForm, 'exchangeForm': exchangeForm}
        return render(request, 'profile.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="forgot-password.html",
                  context={"password_reset_form": password_reset_form})


def logoutUser(request):
    logout(request)
    return redirect('login')
