from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    usable_password = None