from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from knox.models import AuthToken
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_login(request):
    # If user is already logged in redirect to home page
    if request.user.is_authenticated:
        return redirect('authentication:home')

    # If user is not logged in and request method is POST, try to log in the user
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # If user is not None, log in the user
                login(request, user)
                # Redirect to the home page
                return redirect('authentication:home')  # Assuming 'home' is a name of your home URL
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def user_logout(request):
    messages.add_message(request, messages.INFO, "You have been logged out.  So long and thanks for all the fish.")
    logout(request)
    return redirect('authentication:login')

def home(request):
    context = {}
    return render(request, 'authentication/home.html', context)

# Ref https://docs.djangoproject.com/en/5.1/topics/auth/default/#limiting-access-to-logged-in-users
@login_required
def get_tokens(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            # Delete all tokens for the user
            AuthToken.objects.filter(user=request.user).delete()
            # Add a notification message to display to the user
            messages.add_message(request, messages.INFO,"All API tokens have been invalidated.")
            # Render the tokens page
            return render(request, 'authentication/tokens.html', {'tokens': None})
        if request.POST.get('action') == 'create':
            # Create a token for the user via knox
            token = AuthToken.objects.create(request.user)[1]
            # Store the token in the context
            context = {
                'token_created': True,
                'token': token,
            }
            # Add a notification message to display to the user
            messages.add_message(request, messages.INFO, "A new API token has been created.")
            # Render the tokens page with the new token
            return render(request, 'authentication/tokens.html', context)
    else:
        # Retrieve the token from the session
        tokens = AuthToken.objects.filter(user=request.user)
        # Render the tokens page
        return render(request, 'authentication/tokens.html', {'tokens': tokens})


