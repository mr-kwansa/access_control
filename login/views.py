# views.py
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

def home(request):
    return render(request,"login/index.html")
#sigup views
def signup(request):
    # method for getting the information form the fuilds on the html side into the database 
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # make sure that the user name is unique 
        if User.objects.filter(username=username):
            messages.error(request,"Username already exists please try another one")
            return redirect('home')
    
    
        # making suer emails are unique
        if User.objects.filter(email=email):
            messages.error(request,"Email already exists please try another one")
            return redirect('home')
        
        
        # make suer the username is not more than 10 characters long
        if len(username) > 10:
            messages.error(request,"Username is too long must be at most 10 characters")
            
            
            # make sure the passwords match 
        if password  != confirm_password:
            messages.error(request,"Passwords do not match Please try again")
            
            
            # make sure the user name is alfanumeric and nothing else 
        if not username.isalnum():
            messages.error(request,"Username can only contain letters and numbers")
            return redirect('home')
    
    
        # creating a user with the information 
        myuser = User.objects.create_user(username, email,password)
        myuser.first_name = first_name
        myuser.last_name= last_name
        
        
        # okay this one dey save the information about the user 
        myuser.save()
        # basic error handleing
        messages.success(request,"Successfully created user")
        # upon successfullt creating a user take the user to the sigin page    
        return redirect('signin')
         
    return render(request ,"login/signup.html")

# signing view
def signin(request):
    # take information from the user theough the form in the html side
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # user function return none or not none 
        # wrote a function to chek the status and redirect to the main page 
        if user is not None:
            login(request,user)
            first_name=user.first_name   
            return render(request,"login/index.html",{'fname':first_name})
        else:
            messages.error(request,"Details entered for user are incorrenct")
            return redirect('home')
        
    return render(request ,"login/signin.html")

# signout view and logic
def signout(request):
    logout(request)
    messages.success(request,"logged out")
    return redirect("home") 