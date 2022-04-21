from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
UserModel = get_user_model()


def signup(request):
    if request.method == 'GET':
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context=context)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'redirect_email.html')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'confirmed_email.html')
    else:
        return HttpResponse('Activation link is invalid!')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    if user is not None:
                        user = authenticate(request, username=user.username, password=password)
                        if user is not None:
                            login(request, user)
                            return redirect('dashboard')
                        else:
                            messages.error(request, 'Username OR password is incorrect')
                    else:
                        messages.error(request, 'Username OR password is incorrect')
                else:
                    messages.error(request, 'Please check your email and verify your account first')
            except:
                messages.error(request, 'Username OR password is incorrect')
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


@transaction.atomic
@login_required(login_url='login')
def dashboard(request):
    if request.method == 'POST':
        exchangeForm = UserExchangeForm(request.POST)
        assetForm = UserAssetForm(request.POST)
        exchanges = UserExchange.objects.filter(user=request.user)
        if 'ExchangeFormSubmit' in request.POST:
            if len(exchanges) < 3:
                if exchangeForm.is_valid():
                    obj = exchangeForm.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    messages.success(request, ('New exchange added successfully!'))
                    return redirect('dashboard')
                else:
                    messages.error(request, ('Please correct the error in exchanges'))
                    return redirect('dashboard')
        if 'AssetFormSubmit' in request.POST:
            if assetForm.is_valid():
                obj = assetForm.save(commit=False)
                obj.user = request.user
                obj.save()
                messages.success(request, (str(obj.asset) + ' asset added successfully!'))
                return redirect('dashboard')
            else:
                messages.error(request, ('Please correct the error in exchanges'))
                return redirect('dashboard')
    else:

        userForm = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=request.user.profile)
        exchanges = UserExchange.objects.filter(user=request.user)
        exchangeForm = UserExchangeForm(instance=request.user)
        assetForm = UserAssetForm(instance=request.user)
        assets = UserAsset.objects.filter(user=request.user)
        context = {'userForm': userForm, 'profileForm': profileForm, 'exchangeForm': exchangeForm,
                   'assetForm': assetForm, 'exchanges': exchanges, 'assets': assets}
        return render(request, 'dashboard.html', context)


@transaction.atomic
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':

        userForm = UserForm(request.POST, instance=request.user)
        profileForm = ProfileForm(request.POST, instance=request.user.profile)
        if 'UserProfileFormSubmit' in request.POST:
            if userForm.is_valid() and profileForm.is_valid():
                userForm.save()
                profileForm.save()
                messages.success(request, ('Profile updated successfully!'))
                return redirect('dashboard')

            else:
                errors = ProfileForm.errors
                return redirect('profile', json.dumps(errors))

    else:
        userForm = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=request.user.profile)
        exchanges = UserExchange.objects.filter(user=request.user)
        exchangeForm = UserExchangeForm(instance=request.user)
        assetForm = UserAssetForm(instance=request.user)
        assets = UserAsset.objects.filter(user=request.user)
        context = {'userForm': userForm, 'profileForm': profileForm, 'exchangeForm': exchangeForm,
                   'assetForm': assetForm, 'exchanges': exchanges, 'assets': assets}
        return render(request, 'profile.html', context)


class deleteExchange(DeleteView):
    model = UserExchange
    # form_class = UserExchangeForm
    template_name = 'userexchange_confirm_delete.html'
    success_url = reverse_lazy('dashboard')


class deleteAsset(DeleteView):
    model = UserAsset
    # form_class = UserExchangeForm
    template_name = 'userasset_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

@transaction.atomic
@login_required(login_url='login')
def updatePassword(request):
    form = PasswordChangeCustomForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('updatePassword')
    return render(request, 'updatePassword.html', {
        'form': form,
    })


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = UserPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    current_site = get_current_site(request)
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": data,
                        'domain': current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        email = EmailMessage(
                            subject, email, to=[data]
                        )
                        email.send()
                        # send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            else:
                messages.error(request, 'Account with this email not registered. Please check email entered or create new account')
    else:
        password_reset_form = UserPasswordResetForm()
    return render(request=request, template_name="forgot-password.html",
                  context={"password_reset_form": password_reset_form})


@transaction.atomic
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')
