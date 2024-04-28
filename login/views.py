# views.py
import string
import random
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from access_control import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes ,force_str
from . tokens import generatetoken
from .models import AccessKey
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
        myuser.is_active = False
        
        # okay this one dey save the information about the user 
        myuser.save()
        # basic error handleing
        messages.success(request,"Successfully created user")
        # upon successfullt creating a user take the user to the sigin page   
        
        # Sending welcome message via email 
        subject = "Hello Welcome To THE FUTURE OF SAAS"
        message ="Hello "+myuser.first_name+" welcome to Access key management you can go on the site and purchase ypur access key once you activate your account an activation email will be sent to you shortly "
        from_email= settings.EMAIL_HOST_USER
        to_email=[myuser.email]
        # method to send the email
        send_mail(subject, message,from_email,to_email)
        
        # activation of email for user request)ser
        current_site = get_current_site(request)
        email_subject ="Welcome "+myuser.first_name+ ", please click the link below to activate your account"
        email_message = render_to_string('email_confirmation.html', {
                'user': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generatetoken.make_token(myuser),
            })
        
        email = EmailMessage(
                email_subject,
                email_message,
                from_email,
                to_email,
        )
        email.send()
        return redirect('signin')
    
    return render(request, "login/signup.html")

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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generatetoken.check_token(myuser, token):  # Use your custom token generator here
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, 'Your account has been activated successfully. You can now log in.')
        return redirect("home")
    else:
        return render(request, "activationfaild.html")
    
def generate_access_key(request):
    # Check if the user already has an access key
    access_key = AccessKey.objects.filter(user=request.user).first()

    # If an access key already exists for the user, pass it to the template context
    # Otherwise, generate a new access key and save it to the database
    if access_key:
        access_key = access_key.key
    else:
        characters = string.ascii_letters + string.digits + string.punctuation
        access_key = ''.join(random.choice(characters) for _ in range(10))
        AccessKey.objects.create(user=request.user, key=access_key)

    # Pass the access key to the template context
    return render(request, "login/index.html", {'access_key': access_key})