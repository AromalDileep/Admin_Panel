from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
def adminpanel(request):
    users = User.objects.all()
    user_data = []  # A list to hold user data (email and password)
    
    # Loop through users to extract email and password
    for user in users:
        user_data.append({'username': user.username, 'email': user.email})

    return render(request, 'adminpanel.html', {'users': user_data})


def adminlogin(request):
    admin_name = 'admin'
    admin_password = "12345"
    if request.method == 'POST':
        username = request.POST['admin_name']
        password = request.POST['admin_password']
        if username == admin_name and password == admin_password:  
            return redirect('adminpanel')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'adminlogin.html')    


def admin_log_out(request):
      if request.method == 'POST':
          logout(request)
          return redirect('adminlogin')
      return redirect('adminlogin')


def log_in(request):
    if request.user.is_authenticated:
            return redirect('home')
        
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        # Display the login form.
            response =render(request,'login.html')
            response['cache-Control'] = 'no-store'
            return response    
    return render(request, 'login.html')





def home(request):
    if request.user.is_authenticated:
        response =render(request,'home.html')
        response['cache-Control'] = 'no-store'
        return response
    else:
        return redirect(log_in)

 
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:  # Check if all fields are provided
            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            return redirect('login')
        else:
            messages.error(request, "Please fill in all fields")
    return render(request, 'signup.html')


def log_out(request):
      if request.method == 'POST':
          logout(request)
          return redirect('login')
      return redirect('login')


  
def create(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        

        
