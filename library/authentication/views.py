from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required

from authentication.models import CustomUser
from authentication.forms import LoginForm, RegistrationForm, UpdateCustomUserForm


def index_view(request):
    return render(request, 'authentication/index.html')


def register_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You are already logged")
        return redirect('authentication:profile')

    # if request.method == 'POST':
    #     email = request.POST.get('email', '').strip()
    #     password = request.POST.get('password', '')
    #     confirm_password = request.POST.get('confirm_password', '')
    #     first_name = request.POST.get('first_name', '').strip()
    #     last_name = request.POST.get('last_name', '').strip()
    #     middle_name = request.POST.get('middle_name', '').strip()
    #     role = int(request.POST.get('role', 0))

    #     if password != confirm_password:
    #         messages.error(request, 'Passwords do not match.')
    #         return render(request, 'authentication/register.html')

    #     if CustomUser.objects.filter(email=email).exists():
    #         messages.error(request, 'The user with this email already exist.')
    #         return render(request, 'authentication/register.html')

    #     new_user = CustomUser.objects.create_user(
    #         email=email,
    #         password=password,
    #         first_name=first_name,
    #         last_name=last_name,
    #         middle_name=middle_name,
    #         role=role,
    #         is_active=True
    #     )

    #     login(request, new_user)

    #     messages.success(request, 'Registration has been successful!')
    #     return redirect('authentication:index_auth')

    # return render(request, 'authentication/register.html')

    if request.method == 'POST':
            form = RegistrationForm(request.POST)
    
            if form.is_valid():
                new_user = form.save()

                login(request, new_user)

                messages.success(request, 'Registration has been successful!')
                return redirect('authentication:index_auth')
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'authentication/register.html', context=context)


def login_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You are already logged")
        return redirect('authentication:profile')

    # if request.method == 'POST':
    #     email = request.POST.get('email', '').strip()
    #     password = request.POST.get('password', '')

    #     user = authenticate(request, email=email, password=password)

    #     if user is not None:

    #         login(request, user)

    #         messages.success(request, f'Congratulation, {user.email}!')
    #         return redirect('authentication:index_auth')
    #     else:
    #         messages.error(request, 'Invalid email or password.')

    # return render(request, 'authentication/login.html')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.user

            login(request, user)

            messages.success(request, f'Congratulation, {user.email}!')
            return redirect('authentication:index_auth')
    else:
        form = LoginForm(request)

    return render(request, 'authentication/login.html', {'form': form})


@login_required
def logout_view(request):

    logout(request)

    messages.success(request, "Logged out")
    return redirect('authentication:index_auth')


@login_required
def profile_view(request):
    context = {'user_obj': request.user}
    return render(request, 'authentication/profile.html', context=context)


@login_required
def update_profile(request, user_id):

    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user:
        raise PermissionDenied()
    
    # try:
    #     if request.method == 'POST':

    #         user.first_name = request.POST.get('first_name', '').strip()
    #         user.middle_name = request.POST.get('middle_name', '').strip()
    #         user.last_name = request.POST.get('last_name', '').strip()
    #         password = request.POST.get('password', '').strip()

    #         if not password or not password.strip():
    #             password = None

    #         updated_user = user.update(first_name=user.first_name, 
    #                                    middle_name=user.middle_name, 
    #                                    last_name=user.last_name, 
    #                                    password=password)

    #         if password and updated_user:
    #             user.refresh_from_db()
    #             update_session_auth_hash(request, updated_user)
    #     else:
    #         context = {'user':user}
    #         return render(request,'authentication/update_profile.html', context=context)

    # except ValidationError:
    #     messages.error(request, "Incorrect data to change")

    # else:
    #     messages.success(request, "The user successfully updated!")
    #     return redirect('authentication:profile')

    # context = {'user':user}

    # return render(request,'authentication/update_profile.html', context=context)

    if request.method == 'POST':
        form = UpdateCustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, "The user successfully updated!")
            return redirect('authentication:profile')
    else:
        form = UpdateCustomUserForm(instance=user)

    context = {'user': user, 'form': form}

    return render(request,'authentication/update_profile.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def list_of_users_view(request):
    
    users = CustomUser.objects.all()

    context = {'users': users}

    return render(request, 'authentication/list_of_users.html', context=context)


@login_required
@permission_required('is_staff', raise_exception=True)
def user_details_view(request, user_id):

    user = get_object_or_404(CustomUser, pk=user_id)

    context = {'user_obj': user}

    return render(request, 'authentication/user_details.html', context=context)

def bad_request(request, exception=None):
    return render(request, '400.html', status=400)

def permission_denied(request, exception=None):
    return render(request, '403.html', status=403)

def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)