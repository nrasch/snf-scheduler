from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from knox.models import AuthToken

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
                # Create a token for the user via knox
                token = AuthToken.objects.create(user)[1]
                # Store the token in the session
                request.session['knox_token'] = token
                # Redirect to the home page
                return redirect('authentication:home')  # Assuming 'home' is a name of your home URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    messages.add_message(request, messages.INFO, "You have been logged out.  So long and thanks for all the fish.")
    logout(request)
    return redirect('authentication:login')

def home(request):
    # Retrieve the token from the session
    token = request.session.pop('knox_token', None)  # pop removes the key from session

    # Add the token to the context
    context = {
        'token': token,
    }
    return render(request, 'home.html', context)