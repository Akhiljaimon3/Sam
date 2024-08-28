from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import razorpay
from django.utils.crypto import get_random_string
from  django.core.mail import send_mail
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models import Sum
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
import datetime


# Create your views here.

def home(req):
    if 'U_id' in req.session:
        email = req.session.get('U_id')
        user=User.objects.get(email=email)
        duedate=user.Duedate
        
        if duedate is not None:
            if duedate > date.today():
                exp_date = (duedate - date.today()).days
                if exp_date < 6:
                    message = f'Your student concession is expiring in {exp_date} Days'
                else:
                    return render(req,'home.html')
            else:
                message = 'Your student concession has expired.'
            return render(req, 'home.html',{'message':message})
        return render(req,'home.html',)
    return render(req,'home.html',)

def bookyourjourney(req):
    if req.method == 'POST':
        location = req.POST.get('location')
        destination = req.POST.get('destination')
        if location and destination:
            rout = Routes.objects.filter(location=location, destination=destination)
            detail = Route_details.objects.filter(location=location, destination=destination)
            rout = rout.order_by('departure')
            if not rout.exists() and not detail.exists():
                return render(req, 'bookyourjourney.html', {'no_route': True})
            return render(req, 'bookyourjourney.html', {'rout': rout, 'detail': detail})
    return render(req, 'bookyourjourney.html')

def applyforconcession(req):
    if 'U_id' in req.session:
        acs = 1
    else:
        acs = 2

    if req.method == 'POST':
        user_id = req.FILES.get('user_id')
        val = req.POST.get('plan')
        email = req.session['U_id']
        
        # Fetch user data
        user = User.objects.filter(email=email).first()
        if not user:
            return HttpResponse("User not found.")
        name = user.name

        # Determine plan details
        plans = {
            '1/50': {'name': '1 Day Unlimited', 'price': 50},
            '45/495': {'name': '45 Days 50 Rides', 'price': 495},
            'default': {'name': '30 Days Unlimited', 'price': 750}
        }
        
        plan_info = plans.get(val, plans['default'])
        plan_name = plan_info['name']
        amount = plan_info['price']
        
        # Check for discount
        discount = concession_discount.objects.filter(plan=plan_name).first()
        if discount:
            amount = discount.discount_amount
        
        # Create concession record
        concession_data = concession.objects.create(
            name=name,
            email=email,
            userid=user_id,
            plan=plan_name,
            amount=amount,
            status=1
        )
        concession_data.save()
        
        # Redirect with success message
        url = 'watermetro-applyforconcession'
        msg = f'''<script>
            alert('Application completed successfully...');
            window.location='{url}';
        </script>'''
        return HttpResponse(msg)
    
    return render(req, 'applyforconcession.html', {'acs': acs})

def login(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        pas = req.POST.get('password')
        if email == 'admin@kochimetro.com' and pas == 'kochimetro@admin':
            return render(req, 'admin-home.html')
        try:
            x=User.objects.get(email=email)
            if x.password==pas:
                req.session['U_id']=email
                return render(req,'home.html',)
            else:
                messages.error(req, 'Login failed,Invaild password...')
        except:
            messages.error(req, 'Login failed,Invaild username.')
    return render(req,'login.html',)

def signup(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        if User.objects.filter(email=email).exists():
           url = 'watermetro-signup'
           msg = '''<script>alert('email already exist')
                                    window.location='%s'</script>''' % (url)
           return HttpResponse(msg)
        else:
            user = User.objects.create(name=name, email=email, password=password)
            user.save()
            url = 'watermetro-login'
            msg = '''<script>alert('Signup completed successfull')
                                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
    return render(req, 'signup.html')

def logout(req):
    if 'U_id' in req.session:
        req.session.flush()
        return render(req,'home.html',)
    return render(req,'home.html',)

def adminhome(req):
    today = date.today()
    booking = booking_history.objects.filter(bookdate=today)
    concession = concession_history.objects.filter(date=today)
    Vytilla = booking_history.objects.filter(destination='Vytilla',bookdate=today)
    HighCourt = booking_history.objects.filter(destination='HighCourt',bookdate=today)
    Vypin = booking_history.objects.filter(destination='Vypin',bookdate=today)
    Kakkanad = booking_history.objects.filter(destination='Kakkanad',bookdate=today)
    SouthChittoor = booking_history.objects.filter(destination='SouthChittoor',bookdate=today)
    Cheranalloor = booking_history.objects.filter(destination='Cheranalloor',bookdate=today)
    Eloor = booking_history.objects.filter(destination='Eloor',bookdate=today)
    FortKochi = booking_history.objects.filter(destination='FortKochi',bookdate=today)


    Vytilla = Vytilla.aggregate(Sum('amount'))['amount__sum'] or 0
    HighCourt = HighCourt.aggregate(Sum('amount'))['amount__sum'] or 0
    Vypin = Vypin.aggregate(Sum('amount'))['amount__sum'] or 0
    Kakkanad = Kakkanad.aggregate(Sum('amount'))['amount__sum'] or 0
    SouthChittoor = SouthChittoor.aggregate(Sum('amount'))['amount__sum'] or 0
    Cheranalloor = Cheranalloor.aggregate(Sum('amount'))['amount__sum'] or 0
    Eloor = Eloor.aggregate(Sum('amount'))['amount__sum'] or 0
    FortKochi = FortKochi.aggregate(Sum('amount'))['amount__sum'] or 0


    book = booking.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    concess = concession.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    return render(req,'admin-home.html',{'book':book,'today':today,'concess':concess,'Vytilla':Vytilla,'HighCourt':HighCourt,'Vypin':Vypin,'Kakkanad':Kakkanad,'SouthChittoor':SouthChittoor,'Cheranalloor':Cheranalloor,'Eloor':Eloor,'FortKochi':FortKochi,})

def addroute(req):
    if req.method == 'POST':
        location = req.POST.get('location')
        destination = req.POST.get('destination')
        departure = req.POST.get('departure')
        arrival = req.POST.get('arrival')
        if Route_details.objects.filter(location=location,destination=destination).exists():
            data=Routes.objects.create(location=location,destination=destination,departure=departure,Arrival=arrival,status=1)
            data.save
            url = 'addroute'
            msg = '''<script>alert('Route added successfully')
                                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
        else:
            rout=Route_details.objects.create(location=location,destination=destination,travel_time=30,fare=30)
            rout.save()
            data=Routes.objects.create(location=location,destination=destination,departure=departure,Arrival=arrival,status=1)
            data.save
            url = 'addroute'
            msg = '''<script>alert('Route added successfully')
                                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
    return render(req,'admin-addroute.html',)

def editroute(req):
    if req.method == 'POST':
        location = req.POST.get('location')
        destination = req.POST.get('destination')
        if location and destination:
            rout = Routes.objects.filter(location=location, destination=destination)
            detail = Route_details.objects.filter(location=location, destination=destination)
            rout = rout.order_by('departure')
            if not rout.exists() and not detail.exists():
                return render(req, 'admin-editroute.html', {'no_route': True})
            return render(req, 'admin-editroute.html', {'rout': rout, 'detail': detail})
    return render(req,'admin-editroute.html',)

def deleteroute(req):
    if req.method == 'POST':
        location = req.POST.get('location')
        destination = req.POST.get('destination')
        if location and destination:
            rout = Routes.objects.filter(location=location, destination=destination)
            detail = Route_details.objects.filter(location=location, destination=destination)
            rout = rout.order_by('departure')
            if not rout.exists() and not detail.exists():
                return render(req, 'admin-deleteroute.html', {'no_route': True})
            return render(req, 'admin-deleteroute.html', {'rout': rout, 'detail': detail})
    return render(req, 'admin-deleteroute.html')
        
def deleteroutetable(req):
    if req.method == 'POST':
        x = req.POST.get('x')
        if x:
            Routes.objects.filter(id=x).delete()
            return HttpResponse('<script>alert("Route deleted successfully"); window.location="%s"</script>' % req.META.get('HTTP_REFERER'))
    
def editroutelist(request):
    if request.method == 'POST':
        if 'travel_time' in request.POST:
            travel_time = request.POST.get('travel_time')
            fare = request.POST.get('fare')
            x = request.POST.get('x')
            data = Route_details.objects.filter(id=x)
            data.update(travel_time=travel_time, fare=fare)
        elif 'departure' in request.POST:
            departure = request.POST.get('departure')
            Arrival = request.POST.get('Arrival')
            status = request.POST.get('status')
            note = request.POST.get('note')
            x = request.POST.get('x')
            data = Routes.objects.filter(id=x)
            data.update(departure=departure, Arrival=Arrival, status=status,note=note)
        url = 'editroute'
        msg = '''<script>alert('Route updated successfully')
                                    window.location='%s'</script>''' % (url)
        return HttpResponse(msg)
    
def concessionrequests(req):
    data = concession.objects.filter(status=1)
    if req.method == 'POST':
        x = req.POST.get('x')
        status = req.POST.get('status')
        if status == '2':
            data = concession.objects.filter(id=x)
            data.update(status=status)
        elif status =='3':
            data = concession.objects.filter(id=x)
            data.delete()
        data = concession.objects.filter(status=1)
        return render(req,'admin-concessionrequests.html',{'res':data})
    return render(req,'admin-concessionrequests.html',{'res':data})

def aboutus(req):
    return render(req,'aboutus.html',)

def terminalsvytilla(req):
    return render(req,'terminals-vytilla.html',)

def terminalschernalloor(req):
    return render(req,'terminals-chernalloor.html',)

def terminalseloor(req):
    return render(req,'terminals-eloor.html',)

def terminalsfortkochi(req):
    return render(req,'terminals-fortkochi.html',)

def terminalshighcourt(req):
    return render(req,'terminals-highcourt.html',)

def terminalskakkanad(req):
    return render(req,'terminals-kakkanad.html',)

def terminalssouthchitoor(req):
    return render(req,'terminals-southchitoor.html',)

def terminalsvypin(req):
    return render(req,'terminals-vypin.html',)

def editaccount(req):
    acc=1
    email = req.session.get('U_id')
    data = User.objects.filter(email=email)
    if req.method=='POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        x = req.POST.get('x')
        data = User.objects.filter(id=x)
        data.update(name=name, email=email)
        acc=3
        data = User.objects.filter(email=email)
        req.session['U_id']=email
        return render(req,'youraccount.html',{'res':data,'acc':acc})
    return render(req,'youraccount.html',{'res':data,'acc':acc})

def accountchangepassword(req):
    acc=2
    email = req.session.get('U_id')
    data = User.objects.filter(email=email)
    if req.method=='POST':
        password = req.POST.get('password')
        confpassword = req.POST.get('conf-password')
        x = req.POST.get('x')
        if password==confpassword:
            user = User.objects.filter(id=x)
            user.update(password=password)
            url = 'watermetro-youraccount'
            msg = '''<script>alert('Password updated successfully')
                                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
    return render(req,'youraccount.html',{'res':data,'acc':acc})

def youraccount(req):
    email = req.session['U_id']
    data = User.objects.filter(email=email)
    acc=3
    db=1
    conc=concession.objects.filter(email=email)
    tab=booking_history.objects.filter(email=email)
    tab = tab.order_by('-date')
    for i in conc:
        if i.status == 2:
            return render(req,'youraccount.html',{'res':data,'acc':acc,'conc':conc,'tab':tab,'db':db})
        else:
            return render(req,'youraccount.html',{'res':data,'acc':acc,'tab':tab,'db':db})
    return render(req,'youraccount.html',{'res':data,'acc':acc,'tab':tab,'db':db})

def dbchanger(req):
    email = req.session['U_id']
    data = User.objects.filter(email=email)
    acc=3
    db=2
    tab = concession_history.objects.filter(email=email)
    tab = tab.order_by('-date')
    return render(req,'youraccount.html',{'res':data,'acc':acc,'tab':tab,'db':db})

def bookingreport(req):
    # Retrieve all booking history
    tab = booking_history.objects.all()

    # Handle date filtering
    filter_date = req.GET.get('date')
    if filter_date:
        try:
            filter_date = parse_date(filter_date)
            if filter_date:
                tab = tab.filter(bookdate=filter_date)
        except ValueError:
            pass  # Handle invalid date format gracefully

    total_amount = tab.aggregate(total_amount=Sum('amount'))['total_amount']
    total_journeys = tab.count()

    # Default sorting by date in descending order
    tab = tab.order_by('-date')

    # Handle pagination
    paginator = Paginator(tab, 50)  # Show 50 records per page
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(req, 'admin-bookingreport.html', {'tab': page_obj,'selected_date': filter_date,'total_amount': total_amount,'total_journeys': total_journeys})

def concessionreport(req):
    # Retrieve all booking history
    tab = concession_history.objects.all()

    # Handle date filtering
    filter_date = req.GET.get('date')
    if filter_date:
        try:
            filter_date = parse_date(filter_date)
            if filter_date:
                tab = tab.filter(date=filter_date)
        except ValueError:
            pass  # Handle invalid date format gracefully

    total_amount = tab.aggregate(total_amount=Sum('amount'))['total_amount']
    total_journeys = tab.count()

    # Default sorting by date in descending order
    tab = tab.order_by('-date')

    # Handle pagination
    paginator = Paginator(tab, 50)  # Show 50 records per page
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(req, 'admin-concessionreport.html', {'tab': page_obj,'selected_date': filter_date,'total_amount': total_amount,'total_journeys': total_journeys})

def concessionpayment(req,email):
    data = concession.objects.filter(email=email)
    for i in data:
        plan=i.plan
    plans = {
            '1 Day Unlimited': 50,
            '45 Days 50 Rides': 495,
            '30 Days Unlimited': 750}
    amount = plans.get(plan)
    if concession_discount.objects.filter(plan=plan).exists():
        discount = concession_discount.objects.get(plan=plan)
        discount_name = discount.discount_name
        discount_amount = amount-discount.discount_amount
        return render(req,'concession-payment.html',{'res':data,'discount_name':discount_name,'discount_amount':discount_amount})
    return render(req,'concession-payment.html',{'res':data})

def ticketpayment(req):
    if 'U_id' in req.session:
        email = req.session['U_id']
        x = req.POST.get('x')
        y = req.POST.get('y')

        detail= Route_details.objects.filter(id=y)
        data= Routes.objects.filter(id=x)
        user= User.objects.filter(email=email)
        return render(req,'ticket-payment.html',{'res':data,'user':user,'detail':detail})
    else:
        url = 'watermetro-login'
        msg = '''<script>alert('Login first to access this feature')
                                    window.location='%s'</script>''' % (url)
        return HttpResponse(msg)

def concessionpay(request, id):
    plan = request.POST.get('plan')
    request.session['plan'] = plan
    val=id
    amount = id*100
    request.session['amount']=id
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    return render(request, "concession-pay.html",{'r':amount,'val':val})

def ticketpay(request, id):
    if request.method == 'POST':
        location = request.POST.get('location')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        request.session['location'] = location
        request.session['destination'] = destination
        request.session['date'] = date
        val=id
        amount = id * 100
        request.session['amount'] = amount
        client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        return render(request, "ticket-pay.html", {'r': amount,'val':val})
    return render(request, "ticket-pay.html")

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            u = User.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(name=u, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/watermetro-resetpassword/{token}'
        try:
            print("hello")
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
            print("sended")
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot-password.html')

#reset password
def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('password')
        repeat_password = request.POST.get('conf-password')
        if repeat_password == new_password:
            print("new",new_password)
            password_reset.name.password=new_password
            print(password_reset.name.password)
            password_reset.name.save()
            # password_reset.delete()
            url = '/watermetro-login'
            msg = '''<script>alert('Password successfully updated.')
                                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
    return render(request, 'reset-password.html',{'token':token})

# def bookingsuccess(req):
#     bookdate = date.today()
#     email = req.session.get('U_id')
#     amount = req.session.get('amount')/100
#     location = req.session.get('location')
#     destination = req.session.get('destination')
#     dates = req.session.get('date')
#     user = User.objects.get(email=email)
#     name =user.name

#     name_code = f"TN/{name[:3].upper()}"
#     location_code = location[:2].capitalize()
#     destination_code = destination[:2].capitalize()
#     date_code = bookdate.strftime("%d%m%y")
#     additional_code = f"-{location_code}/{destination_code}{date_code}"
#     secretcode = f"{name_code}{additional_code}"

#     data = booking_history.objects.create(name=name, email=email, location=location,destination=destination,amount=amount,date=dates,bookdate=bookdate,secretcode=secretcode)
#     data.save()
#     return render(req, 'booking-success.html',{'location':location,'destination':destination,'amount':amount,'dates':dates,'secretcode':secretcode})

# def concessionsuccess(req):
#     dates = date.today()
#     email = req.session.get('U_id')
#     amount = req.session.get('amount')
#     plan = req.session.get('plan')
#     user = User.objects.get(email=email)
#     user1 = User.objects.filter(email=email)
#     name =user.name

#     name_code = f"CN/{name[:3].upper()}"
#     date_code = dates.strftime("%d%m%y")
#     additional_code = f"-{date_code}"
#     secretcode = f"{name_code}{additional_code}"

#     data = concession_history.objects.create(name=name, email=email, plan=plan,amount=amount,date=dates,secretcode=secretcode)
#     data.save()

#     plans = {
#             '45 Days 50 Ridess': 45,
#             '30 Days Unlimiteds': 30}
#     day = plans.get(plan)
#     duedate = dates + timedelta(days=day)
#     user1.update(Duedate=duedate)
#     # conces = concession.objects.get(email=email)
#     # conces.delete()
#     return render(req,'concession-success.html',{'name':name,'email':email,'amount':amount,'date':dates,'plan':plan,'secretcode':secretcode})

def concessiondiscount(req):
    if req.method == 'POST':
        plan_code = req.POST.get('plan')
        discountname = req.POST.get('discountname')
        discountamount = req.POST.get('discountamount')
        discountpercentage = req.POST.get('discountpercentage')
        
        plans = {
            '1/50': {'name': '1 Day Unlimited', 'price': 50},
            '45/495': {'name': '45 Days 50 Rides', 'price': 495},
            'default': {'name': '30 Days Unlimited', 'price': 750}
        }
        
        plan_info = plans.get(plan_code, plans['default'])
        plan_name = plan_info['name']
        original_price = plan_info['price']
        
        # Calculate discount amount
        if discountamount:
            amount = original_price - float(discountamount)
        elif discountpercentage:
            discount = (original_price / 100) * float(discountpercentage)
            amount = original_price - discount
        else:
            url = 'concessiondiscount'
            msg = '''<script>alert('No discount amount or percentage provided.')
                                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
        
        concession_discount.objects.filter(plan=plan_name).delete()
        concession_discount.objects.create(
            plan=plan_name,
            discount_amount=amount,
            discount_name=discountname
        )
        
        url = 'concessiondiscount'
        msg = f'''<script>
            alert('Concession discount added successfully...');
            window.location='{url}';
        </script>'''
        return HttpResponse(msg)
    data = concession_discount.objects.all()
    return render(req, 'admin-concessiondiscount.html',{'res':data})

def ticketview(req):
    if req.method == 'POST':
        location = req.POST.get('location')
        destination = req.POST.get('destination')
        date = req.POST.get('date')
        amount = req.POST.get('amount')
        secretcode = req.POST.get('secretcode')
        return render(req,'ticketview.html',{'location':location,'destination':destination,'amount':amount,'date':date,'secretcode':secretcode})
    return render(req,'ticketview.html',)

def concessionview(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        date = req.POST.get('date')
        amount = req.POST.get('amount')
        plan = req.POST.get('plan')
        secretcode = req.POST.get('secretcode')
        return render(req,'concessionview.html',{'name':name,'email':email,'amount':amount,'date':date,'plan':plan,'secretcode':secretcode})
    return render(req,'concessionview.html',)

def deletediscount(req):
    if req.method == 'POST':
        x = req.POST.get('x')
        if x:
            concession_discount.objects.filter(id=x).delete()
            return HttpResponse('<script>alert("Discount deleted successfully"); window.location="%s"</script>' % req.META.get('HTTP_REFERER'))
    return render(req, 'admin-concessiondiscount.html')


def generate_ticket_image(location, destination, amount, dates, secretcode):
    # Load the base image
    base_image_path = "C:/Akhil_Project/WaterMetro/Assets/images/ticket_image.png"
    base = Image.open(base_image_path).convert('RGBA')

    # Create a drawing context
    draw = ImageDraw.Draw(base)

    # Define your fonts with default fallback
    try:
        font_path = "C:/Windows/Fonts/arial.ttf"  # Path to regular Arial font
        font_bold_path = "C:/Windows/Fonts/arialbd.ttf"  # Path to bold Arial font
        font_medium = ImageFont.truetype(font_path, 30)  # Medium font size for "From" and "To"
        font_large = ImageFont.truetype(font_path, 40)  # Large font size for main text
        font_amount = ImageFont.truetype(font_bold_path, 75)  # Larger bold font size for amount
    except IOError:
        font_small = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_amount = ImageFont.load_default()  # Fallback for larger font size if custom is not available

    # Draw text on the image with the specified positions
    # Adjust coordinates based on the new font size
    # "From" and "To" with medium font size
    draw.text((base.width * 0.08, base.height * 0.05), "From", font=font_medium, fill="#a09f9f")
    draw.text((base.width * 0.08, base.height * 0.10), f"{location}", font=font_large, fill="black")
    
    draw.text((base.width * 0.08, base.height * 0.18), "To", font=font_medium, fill="#a09f9f")
    draw.text((base.width * 0.08, base.height * 0.23), f"{destination}", font=font_large, fill="black")
    
    # Use the bold font for amount
    draw.text((base.width * 0.10, base.height * 0.40), f"{amount}₹", font=font_amount, fill="black")
    
    draw.text((base.width * 0.10, base.height * 0.55), "Date", font=font_medium, fill="#a09f9f")
    draw.text((base.width * 0.10, base.height * 0.60), f"{dates}", font=font_large, fill="black")
    
    draw.text((base.width * 0.35, base.height * 0.71), f"{secretcode}", font=font_large, fill="black")

    # Save image to a BytesIO object
    img_io = io.BytesIO()
    base.save(img_io, format='PNG')
    img_io.seek(0)

    return ContentFile(img_io.read(), 'ticket.png')

def bookingsuccess(req):
    bookdate = date.today()
    email = req.session.get('U_id')
    amount = req.session.get('amount')/100
    location = req.session.get('location')
    destination = req.session.get('destination')
    dates = req.session.get('date')
    user = User.objects.get(email=email)
    name = user.name

    name_code = f"TN/{name[:3].upper()}"
    location_code = location[:2].capitalize()
    destination_code = destination[:2].capitalize()
    date_code = bookdate.strftime("%d%m%y")
    additional_code = f"-{location_code}/{destination_code}{date_code}"
    secretcode = f"{name_code}{additional_code}"

    data = booking_history.objects.create(
        name=name, email=email, location=location,
        destination=destination, amount=amount,
        date=dates, bookdate=bookdate, secretcode=secretcode
    )
    data.save()

    # Generate the ticket image
    ticket_image = generate_ticket_image(location, destination, amount, dates, secretcode)

    # Create email
    email_subject = 'Your Booking Ticket'
    email_body = 'Thank you for your booking. Please find your ticket attached.'
    email_message = EmailMessage(
        email_subject,
        email_body,
        'settings.EMAIL_HOST_USER',
        [email]
    )
    email_message.attach(ticket_image.name, ticket_image.read(), 'C:/Akhil_Project/WaterMetro/Assets/images/ticket_image.png')
    email_message.send()

    return render(req, 'booking-success.html', {
        'location': location,
        'destination': destination,
        'amount': amount,
        'dates': dates,
        'secretcode': secretcode
    })

def generate_concession_image(name, email, plan, amount, date, secretcode):
    # Convert date to string if it's a datetime.date object
    if isinstance(date, datetime.date):
        date = date.strftime('%Y-%m-%d')  # Format date as a string (e.g., '2024-08-14')

    # Load the base image
    base_image_path = "C:/Akhil_Project/WaterMetro/Assets/images/concession_bill.png"  # Update this path if needed
    base = Image.open(base_image_path).convert('RGBA')

    # Create a drawing context
    draw = ImageDraw.Draw(base)

    # Define your fonts with default fallback
    try:
        font_path = "C:/Windows/Fonts/arial.ttf"  # Path to regular Arial font
        font_bold_path = "C:/Windows/Fonts/arialbd.ttf"  # Path to bold Arial font
        font_email = ImageFont.truetype(font_path, 35)  # Font size for email
        font_from = ImageFont.truetype(font_path, 45)  # Font size for "From" and "To"
        font_plan = ImageFont.truetype(font_path, 30)  # Font size for "Plan" and plan
        font_amount = ImageFont.truetype(font_bold_path, 75)  # Bold font size for amount
        font_date = ImageFont.truetype(font_path, 30)  # Font size for date
        font_secretcode = ImageFont.truetype(font_path, 40)  # Font size for secret code
    except IOError:
        font_email = ImageFont.load_default()
        font_from = ImageFont.load_default()
        font_plan = ImageFont.load_default()
        font_amount = ImageFont.load_default()
        font_date = ImageFont.load_default()
        font_secretcode = ImageFont.load_default()

    # Draw text on the image with the specified positions
    draw.text((base.width * 0.08, base.height * 0.06), name, font=font_from, fill="black")  # Name as "From"
    draw.text((base.width * 0.08, base.height * 0.11), email, font=font_email, fill="#a09f9f")  # Email

    draw.text((base.width * 0.08, base.height * 0.20), "Plan", font=font_plan, fill="#a09f9f")  # "Plan"
    draw.text((base.width * 0.08, base.height * 0.25), plan, font=font_secretcode, fill="black")  # Plan

    draw.text((base.width * 0.10, base.height * 0.40), f"{amount}₹", font=font_amount, fill="black")  # Amount

    draw.text((base.width * 0.10, base.height * 0.55), "Date", font=font_date, fill="#a09f9f")  # "Date"
    draw.text((base.width * 0.10, base.height * 0.60), date, font=font_secretcode, fill="black")  # Date

    draw.text((base.width * 0.35, base.height * 0.71), secretcode, font=font_secretcode, fill="black")  # Secret Code

    # Save image to a BytesIO object
    img_io = io.BytesIO()
    base.save(img_io, format='PNG')
    img_io.seek(0)

    return ContentFile(img_io.read(), 'concession.png')

def concessionsuccess(req):
    dates = date.today()
    email = req.session.get('U_id')
    amount = req.session.get('amount')
    plan = req.session.get('plan')
    user = User.objects.get(email=email)
    user1 = User.objects.filter(email=email)
    name =user.name

    name_code = f"CN/{name[:3].upper()}"
    date_code = dates.strftime("%d%m%y")
    additional_code = f"-{date_code}"
    secretcode = f"{name_code}{additional_code}"

    data = concession_history.objects.create(name=name, email=email, plan=plan,amount=amount,date=dates,secretcode=secretcode)
    data.save()
    olddata=concession.objects.filter(email=email)
    olddata.delete()
    if plan != '1 Day Unlimited':
        plans = {
        '45 Days 50 Rides': 45,
        '30 Days Unlimited': 30
        }
    
        day = plans.get(plan)
    
        if day is not None:
            duedate = dates + timedelta(days=day)
            user1.update(Duedate=duedate)

    concession_image = generate_concession_image(name, email, plan, amount, dates, secretcode)

    # Create email
    email_subject = 'Your Concession card'
    email_body = 'Thank you for using online concession. Please find your concession attached.'
    email_message = EmailMessage(
        email_subject,
        email_body,
        'settings.EMAIL_HOST_USER',
        [email]
    )
    email_message.attach(concession_image.name, concession_image.read(), 'C:/Akhil_Project/WaterMetro/Assets/images/concession_bill.png')
    email_message.send()

    return render(req,'concession-success.html',{'name':name,'email':email,'amount':amount,'date':dates,'plan':plan,'secretcode':secretcode})

