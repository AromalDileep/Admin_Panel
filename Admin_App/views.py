from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Admin login view
def adminlogin(request):
    admin_name = 'admin'
    admin_password = '12345'
    if request.method == 'POST':
        username = request.POST['admin_name']
        password = request.POST['admin_password']
        if username == admin_name and password == admin_password:
            request.session['admin_logged_in'] = True  # Set custom session variable
            return redirect('adminpanel')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'adminlogin.html')

# Admin panel view with cache control
@never_cache
def adminpanel(request):
    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    # Retrieve all users
    users = User.objects.all()
    user_data = []  # A list to hold user data (username and email)

    # Loop through users to extract username and email
    for user in users:
        user_data.append({'username': user.username, 'email': user.email})

    # Render the admin panel template with the user data
    response = render(request, 'adminpanel.html', {'users': user_data})
    response['Cache-Control'] = 'no-store'  # Prevent caching
    return response

# Admin logout view
def adminlogout(request):
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    response = redirect('adminlogin')
    response['Cache-Control'] = 'no-store'  # Prevent caching
    return response

# User signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:  # Check if all fields are provided
            User.objects.create_user(username, email, password).save()
            return redirect('login')
        else:
            messages.error(request, "Please fill in all fields")
    return render(request, 'signup.html')

# User login view
def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    # Display the login form
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store'
    return response

# Home view
def home(request):
    if request.user.is_authenticated:
        response = render(request, 'home.html')
        response['Cache-Control'] = 'no-store'
        return response
    else:
        return redirect(log_in)

# User logout view
def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('login')


# Create user view (it seems incomplete, needs more context to complete this function)
def create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            User.objects.create_user(username, email, password).save()
            messages.success(request, "User created successfully")
            return redirect('home')
        else:
            messages.error(request, "Please fill in all fields")
    return render(request, 'create.html')
