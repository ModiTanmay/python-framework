from django.shortcuts import render,redirect
from .models import Contact,User
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.
def index(request):
	return render(request,'index.html')


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks'],
        )
        msg = "Contact Saved Successfully" 
        contacts=Contact.objects.all().order_by("-id")[:3]
        return render(request, 'contact.html', {'msg': msg,'contacts':contacts})
    else:
     contacts=Contact.objects.all().order_by("-id")[:3]  

    return render(request, 'contact.html', {'contacts':contacts}) 


def signup(request):

    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email is Alredy Registered"
            return render(request, 'signup.html', {'msg':msg})

        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    )
                msg="User Sign Up Successfully"
                return render(request, 'signup.html',{'msg':msg})
            else:
                msg="password & Cornfirm Password does not matched"
                return render(request, 'signup.html', {'msg':msg})






    else:
        return render(request,'signup.html')

	

def login(request):

    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'index.html')

            else:
                msg="Invalid Password"
                return render(request,'login.html',{'msg':msg})

        except:
            msg="Email is not Registered"
            return render(request,'login.html',{'msg':msg})



    else:
        return render(request,'login.html')


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request,'login.html')

    except:
        return render(request,'login.html')


def change_password(request): 
    user=User.objects.get(email=request.session['email'])

    if request.method=="POST":
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg="New Password & Cornfirm New password Does not matched "
                return render(request,'change-password.html',{'msg':msg})

        else:
                msg="Old password Does not matched "
                return render(request,'change-password.html',{'msg':msg})



    else:
        return render(request,'change-password.html')


def forgot_password(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            subject = 'OTP For forgot Password'
            otp=random.randint(1000,9999)
            message = 'Hello'+user.fname+", Your OTP for Forgot Password is"+str(otp)            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html',{'otp':otp,'email':user.email})

        except:
            msg="Email is not Registered"
            return render(request,'forgot-password.html',{'msg':msg})


    else:
        return render(request,'forgot-password.html')

def verify_otp(request):
    email= request.POST['email']
    otp=request.POST['otp']
    uotp=request.POST['uotp']



    if otp==uotp:
        return render(request,'new-password.html',{'email':email})

    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})


def new_password(request):
    email=request.POST['email']
    np=request.POST['n_password']
    cnew=request.POST['cn_password']
    
    if np==cnew:
        user=User.objects.get(email=email)
        user.password=np
        user.save()
        return redirect('login')

    else:
        msg="New Password And Cornfirm New Password Does Not Matched"
        return render(request,'new-password.html',{'email':email,'msg':msg})









   
    

    


