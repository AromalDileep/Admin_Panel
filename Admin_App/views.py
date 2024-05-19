from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
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

    # Render the admin panel template with the user data
    response = render(request, 'adminpanel.html', {'users': users})
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
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
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

# Create user view
def create(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:  # Check if all fields are provided
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                User.objects.create_user(username, email, password).save()
                return redirect('adminpanel')
        else:
            messages.error(request, "Please fill in all fields")
    return render(request, 'create.html')


def edituser(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email:  # Check if required fields are provided
            user.username = username
            user.email = email
            if password:
                user.set_password(password)

            user.save()
            messages.success(request, "User updated successfully")
            return redirect('adminpanel')
        else:
            messages.error(request, "Please fill in all required fields")

    return render(request, 'edit.html', {'user': user})

    
