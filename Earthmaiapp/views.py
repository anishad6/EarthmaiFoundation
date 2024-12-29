from django.conf import settings
from django.shortcuts import render ,redirect,get_object_or_404
from Earthmaiapp.models import GalleryImage,BeachImage, PartnershipRequest,SocialImage,AboutCard, Advisor,Initiative,InvolvementOption,Donation,Volunteer,PartnershipRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
import string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
import razorpay
from Earthmaiapp.models import PasswordResetOTP
# import razorpay 

# Create your views here.
def home(request):
    # context={}
    # data=Project.objects.all()
    # context['project']=data
    initiatives = Initiative.objects.all()
    print(initiatives)
    context={}
    context['initiatives']=initiatives
    return render(request, 'index.html',context)
            
def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        context={}
        u = request.POST['username']   #username entered by user must be unique.
        e= request.POST['email']
        p= request.POST['password']
        cp= request.POST['confirmpassword']
        print(u,e,p,cp)
        if u=='' or e=='' or p=='' or cp=='':
            context['error']='Please fill all the details'
            return render(request,'register.html',context)
        elif p != cp:
            context['error']='Password & Confirm Password must be same'
            return render(request,'register.html',context)
        elif User.objects.filter(username=u).exists():
            context['error']='Username already exist. Enter unique username'
            return render(request,'register.html',context)
        elif u.isnumeric():
            context['error'] = 'Username cannot be a number'
            return render(request, 'register.html', context)
        # elif not phone.isdigit():
        #     context['error'] = 'Phone number must contain only digits'
        #     return render(request, 'register.html', context)
        else: 
            user=User.objects.create(username=u,email=e) #add the data in db
            user.set_password(p)  # password encryption
            user.save()
            # context['success']='Registration Successfully!!! Please Login'
            # return render(request,'login.html',context)
            messages.success(request,'Registration Successfully!!! Please Login')
            return redirect('/login')


def userLogin(request):  # name cant be login 
    context={}
    # context["types"]= categories
    if request.method=="GET":
        return render(request,"login.html",context)
    else:
        context={}
        # user login code
        u=request.POST['username']
        p=request.POST["password"]
        user=authenticate(username=u, password=p)
        if user is None:
            print("wrong cred")
            context["error"]="Invalid username or password"
            return render(request,"login.html",context)
        else:
            print("successfully")
            login(request,user)
            messages.success(request,"Logged in successfully!!")

            return redirect("/")

def userLogout(request):
    logout(request)
    messages.success(request,"Logged out successfully!!")
    return redirect("/")


def about(request):
    cards = AboutCard.objects.all()
    advisors = Advisor.objects.all()
    return render(request, 'about.html', {'cards': cards, 'advisors': advisors})
    # return render(request,"about.html")

# def about(request):
#     advisors = Advisor.objects.all()
#     return render(request, 'about.html', {'advisors': advisors})

def get_involved(request):
    involvement_options = InvolvementOption.objects.all()
    return render(request, 'get_involved.html', {'involvement_options': involvement_options})
    # return render(request,"get_involved.html")


def tree_plantation(request):
    images = GalleryImage.objects.all()  # Fetch all images from the database
    context={'images':images}
    return render(request,'tree_plantation.html',context)

    
def beach(request):
    images = BeachImage.objects.all()  # Fetch all images from the database
    context={'images':images}
    return render(request, 'beach.html',context)

def social(request):
    images = SocialImage.objects.all()  # Fetch all images from the database
    return render(request, 'social.html', {'images': images})

def initiatives_list(request):
    initiatives = Initiative.objects.all()
    print(initiatives)
    context={}
    context['initiatives']=initiatives
    return render(request, 'initiatives_list.html',context)
    # return render(request, 'what we do.html', {'initiatives': initiatives})


def volunteer_details_view(request):
    # Assuming "Volunteer" options are stored in the same model with a specific filter
    volunteer_options = InvolvementOption.objects.filter(title__icontains="Volunteer")
    return render(request, 'volunteer.html', {'options': volunteer_options})



def donate(request):
    """
    Displays the donation form.
    Logged-out users can view the form, but they will be redirected to the 
    registration page when they attempt to donate.
    """
    return render(request, "enteramount.html")


def process_payment(request):
    """
    Processes the donation form submission.
    Redirects users to the registration page if they are not logged in.
    """
    if not request.user.is_authenticated:
        # Redirect to the registration page if the user is not logged in
        messages.warning(request, "Please log in or register to donate.")
        return redirect("login")  # Replace "register" with your registration URL name

    if request.method == "POST":
        # Retrieve data from the form
        amount_in_rupees = float(request.POST["amount"])  # Amount entered in rupees
        message = request.POST.get("message", "")

        # Save the amount (in rupees) and message to the Donation model
        donation = Donation.objects.create(
            user=request.user,
            amount=amount_in_rupees,  # Save amount in rupees
            message=message,
        )

        # Convert amount to paise for Razorpay (multiply by 100)
        amount_in_paise = int(amount_in_rupees * 100)

        # Razorpay Client Setup
        client = razorpay.Client(auth=("rzp_test_QPXTPF1KYwWdC0", "QrLzjZkppijznBLWFiAnmDSt"))

        # Create Razorpay Order
        razorpay_order = client.order.create({
            "amount": amount_in_paise,  # Pass the amount in paise here
            "currency": "INR",
            "receipt": f"receipt_{donation.id}"  # Use donation ID as receipt identifier
        })

        # Sending email
        send_mail(
            subject="Thank You for Your Donation",
            message=f"Dear {request.user.username},\n\n"
                    f"Thank you for your generous donation of ₹{amount_in_rupees}.\n"
                    f"Your support helps us make a difference!\n\n"
                    f"Message: {message}\n\n"
                    "Best regards,\nYour Team",
            from_email='nishadabhishek200027@gmail.com',
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        messages.success(request, "Thank you for your donation!")

        # Pass order details to the Razorpay button template
        context = {
            "amount": amount_in_rupees,  # Pass amount in rupees for display
            "order_id": razorpay_order["id"],  # Razorpay Order ID
            "key": "rzp_test_QPXTPF1KYwWdC0",  # Razorpay API Key
        }
        return render(request, "razorpay_button.html", context)

    return redirect("donate")


def success(request):
    """
    Displays a success message after the donation is completed.
    """
    return render(request, "success.html")

#  Volunteer fuction 

def volunteer_form(request):
    if request.method == "POST":
        # Retrieve data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Initialize a context dictionary for error handling
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
        }
        
        if name=='' or email=='' or phone=='' or message=='':
            context['error']='Please fill all the details'
            return render(request,'volunteer.html',context)
        # Validate name and phone number
        elif name.isnumeric():
            context['error'] = 'Username cannot be a number'
            return render(request, 'volunteer.html', context)
        elif not phone.isdigit():
            context['error'] = 'Phone number must contain only digits'
            return render(request, 'volunteer.html', context)

        # Save data to the database
        volunteer = Volunteer(name=name, email=email, phone=phone, message=message)
        volunteer.save()

        return redirect('success1')
    else:
        return render(request, 'volunteer.html')

def volSuccess(request):
    return render(request, 'success1.html')


def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin_dashboard/index.html')
    else:
        return redirect('login')



def partner_with_us(request):
    if request.method == 'POST':
        # Retrieve data from the form
        company_name = request.POST.get('company_name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Initialize context to retain input and display errors
        context = {
            'company_name': company_name,
            'contact_person': contact_person,
            'email': email,
            'message': message,
        }

        # Validate form inputs
        if not company_name or not contact_person or not email or not message:
            context['error'] = 'All fields are required. Please fill out all the details.'
            return render(request, 'partner_with_us.html', context)

        if contact_person.isnumeric():
            context['error'] = 'Contact person name cannot be numeric.'
            return render(request, 'partner_with_us.html', context)

        if '@' not in email or '.' not in email:
            context['error'] = 'Enter a valid email address.'
            return render(request, 'partner_with_us.html', context)

        # Save data to the database
        partner = PartnershipRequest(
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            message=message
        )
        partner.save()

        # Success message and redirect
        context['success'] = 'Thank you for reaching out to us. We will get back to you soon!'
        return render(request, 'partner_with_us.html', context)

    return render(request, 'partner_with_us.html')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No account found with that email.")
            return render(request, "forgot_password.html")

        for user in users:
            # Generate an OTP
            otp = ''.join(random.choices(string.digits, k=6))
            PasswordResetOTP.objects.update_or_create(user=user, defaults={"otp": otp})

            # Send the OTP via email
            send_mail(
                "Password Reset OTP",
                f"Hello {user.username},\n\nYour OTP for resetting the password is: {otp}.\n\nUse this to reset your password.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        messages.success(request, "An OTP has been sent to your email.")
        return redirect('enter_otp')  # Redirect to the OTP entry page
    return render(request, "forgot_password.html")


def enter_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")

        try:
            reset_entry = PasswordResetOTP.objects.get(otp=otp)
            # Save the user ID in session to use it in the reset password view
            request.session['reset_user_id'] = reset_entry.user.id
            return redirect('reset_password')
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            return render(request, "enter_otp.html")

    return render(request, "enter_otp.html")


# Reset Password View

def reset_password(request):
    user_id = request.session.get('reset_user_id')

    if not user_id:
        messages.error(request, "Unauthorized access. Please restart the process.")
        return redirect('forgot_password')

    try:
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
            else:
                user.set_password(password)
                user.save()
                del request.session['reset_user_id']  # Clear session after password reset
                messages.success(request, "Your password has been reset successfully. You can now log in.")
                return redirect('login')
    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('forgot_password')

    return render(request, 'reset_password.html')
