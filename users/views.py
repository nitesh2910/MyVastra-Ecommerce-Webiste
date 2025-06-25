from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistrationForm, UserProfileForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    try:
        return render(request, 'users/profile.html', {'profile': request.user.userprofile})
    except Exception as e:
        messages.error(request, f"Error loading profile: {str(e)}")
        return redirect('home')


@login_required
def profile_edit_view(request):
    try:
        profile = request.user.userprofile
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = UserProfileForm(instance=profile)
        return render(request, 'users/profile_edit.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Unable to load/edit profile: {str(e)}")
        return redirect('profile')
