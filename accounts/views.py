from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import MyUserCreationForm


def register(request):
    # if user data was submitted, process the data and return to other page
    if request.method == 'POST':
        form = MyUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:index')
        else:
            print("Warning: form not valid")

    # else return an empty form for the user to fill in data
    return render(request, template_name='registration/register.html', context={'form': MyUserCreationForm()})