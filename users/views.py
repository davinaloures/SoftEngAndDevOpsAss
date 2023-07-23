from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #creates instance of form with POST data if there's a POST request
        if form.is_valid(): #validation of form
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You are now able to log in')
            return redirect ('login') #redirecting to home page after account creation
    else:
        form = UserRegisterForm() #creating instance of user creation form (empty)
    return render(request, 'users/register.html', {'form': form})

@login_required() #profile decorator so that only logged-in users can navigate to profile page. Redirected to log in instead and will redirect back to profile after login
def profile(request):
    #conditional if POST request is run, then forms are instantiated
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        #conditional so that data is only saved if both the forms are valid
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


    