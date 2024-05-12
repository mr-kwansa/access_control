# views.py
import string
import random
from datetime import timedelta 
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
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
        from_email = settings.EMAIL_HOST_USER
        to_email = [myuser.email]

        message_body = (
             "Hello " + myuser.first_name + "!\n" +
             "Welcome to The Access key Managment system.\n" +
             "Please click the link below to activate your account.\n" +
             render_to_string('email_confirmation.html', {
            'domain': get_current_site(request),
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generatetoken.make_token(myuser),
        })
            )

        send_mail(subject, message_body, from_email, to_email, fail_silently=False)

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
            # first_name=user.first_name 
            if user.is_staff:
                return redirect('micro_focus_admin')
            else:
                return render(request,"login/index.html",{'user':user})
        else:
            messages.error(request,"Details entered for user are incorrenct")
            return redirect('home')
        
        

    return render(request ,"login/signin.html",)

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
    

@login_required
def generate_access_key(request):
    # Check if the user already has an access key
    access_key_instance = AccessKey.objects.filter(user=request.user).first()

    # If an access key already exists for the user, use it; otherwise, generate a new one
    if access_key_instance:
        access_key = access_key_instance.key
        created_at = access_key_instance.created_at
        expiration_date = access_key_instance.expiration_date
        is_active=access_key_instance.is_active
    else:
        characters = string.ascii_letters + string.digits + string.punctuation
        access_key = ''.join(random.choice(characters) for _ in range(30))
        created_at = timezone.now()
        expiration_date = created_at + timedelta(days=180)
        is_active = True
        access_key_instance =AccessKey.objects.create(user=request.user, 
                                                       key=access_key, 
                                                       created_at=created_at, 
                                                       expiration_date=expiration_date,
                                                       is_active=is_active)

    # Pass the access key and its details to the template context
    return render(request, "login/index.html", {'access_key_instance': access_key_instance.key, 'created_at': created_at, 'expiration_date': expiration_date ,'is_active':is_active})

@staff_member_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')  # Ensures the user is staff
def micro_focus_admin(request):
    # Query all users and their associated access keys
    users_with_keys = []
    users = User.objects.all()
    for user in users:
        access_key = AccessKey.objects.filter(user=user).first()
        users_with_keys.append({'user': user, 'access_key': access_key})

    return render(request, 'login/micro_focus_admin.html', {'users_with_keys': users_with_keys})


@staff_member_required
def toggle_access_key_status(request, access_key_id):
    # Retrieve the access key object
    access_key = AccessKey.objects.get(id=access_key_id)

    # Toggle the is_active status
    access_key.is_active = not access_key.is_active
    access_key.save()

    return redirect('micro_focus_admin')



def micro_focus_admin_api(request):
    # Query all users and their associated access keys
    users_with_keys = []
    users = User.objects.all()
    for user in users:
       access_key = AccessKey.objects.filter(user=user).first()
       users_with_keys.append({
                            'user': user.username,
                            'user_email': user.email,
                            'user_accesskey_is_active': access_key.is_active if access_key else False,
                            'access_key_date_created': access_key.created_at if access_key else None,
                            'access_key_date_expire': access_key.expiration_date if access_key else None,
                            'access_key': access_key.key if access_key else "N/A"
})


    # Return the data as JSON response
    return JsonResponse({'users_with_keys': users_with_keys})

    
def school_integration_endpoint(request):
    if request.method == 'POST':
        
        email =request.POST['email']
        
        user = User.objects.filter(email=email).first()
        if user:
            access_key = AccessKey.objects.filter(user=user,is_active=True).first()
            
            if access_key:
                response_data={
                    'status': 'success',
                    'message':'Successfully authenticated',
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'active_key':access_key.key,
                        'creation_date':access_key.created_at,
                        'expiration_date':access_key.expiration_date,
                        
                    }
                }
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({'status':'error','message':'NO Active key found'})
        else:
            return JsonResponse({'status':'error','message':'User not found'},status=404)
    return render(request,'login/school_integration_endpoint.html')