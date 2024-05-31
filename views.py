from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Product, Cart, Order, ContactSubmission
import random
from .forms import ContactForm
from django.http import HttpResponseRedirect
import razorpay
from django.core.mail import send_mail

def home(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,":",upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,'index.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid username/password!"
                return render(request,'index.html',context)
    else:
        return render(request,'index.html')

    userid=request.user.id
    uname=request.user.username
    print("User id is:",userid)
    print("Username:",uname)
    print("Result is:",request.user.is_authenticated)
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    print(p)
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(userid)
        #print(pid)
        u=User.objects.filter(id=userid)
        print(u[0])
        p=Product.objects.filter(id=pid)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        print(n)
        context={}
        context['products']=p
        if n==1:
            context['msg']="Product already exists in cart!!"
            return render(request,'product_details.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product successfully added to Cart!!"
            return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    c = Cart.objects.filter(uid=request.user.id)
    if not c:
        # Handle the case when the cart is empty
        context = {}
        context['items'] = 0
        context['total'] = 0
        context['data'] = []
        return render(request, 'viewcart.html', context)

    # At this point, c is not empty, so it's safe to access its elements
    s = 0
    for x in c:
        s += x.pid.price * x.qty
    np = len(c)
    context = {}
    context['items'] = np
    context['total'] = s
    context['data'] = c
    return render(request, 'viewcart.html', context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c)   
    print(c[0])
    print(c[0].qty)   #1
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    np=len(orders)
    context['items']=np
    context['total']=s
    return render(request,'placeorder.html',context)



def remove(request,uid):
    c=Cart.objects.filter(id=uid)
    c.delete()
    return redirect('/viewcart')
 
    
def pdetails(request, pid):
    p = Product.objects.filter(id=pid)
    print(p)
    context = {'products': p}
    return render(request, 'product_details.html', context)


def contact(request):
    context = {}  # Define the context dictionary
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create a new ContactSubmission object and save it
            contact_submission = ContactSubmission(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                message=form.cleaned_data['message']
            )
            contact_submission.save()
            
            # Redirect to a success page after successful submission
            context['success'] = "Thanks for Submitting!!"
            return HttpResponseRedirect('/home')  # Change this to your thank-you page URL
    
    else:
        form = ContactForm()
    
    context['form'] = form  # Add the form to the context dictionary
    return render(request, 'contact.html', context)
    
def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        print(uname,upass,ucpass)
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Pass and confirm pass not matching"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User registered Successfully! Please go ahead and login!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already Registered,use a different Id!"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    userid = request.user.id
    uname = request.user.username
    print("User id is:", userid)
    print("Username:", uname)
    print("Result is:", request.user.is_authenticated)
    context = {}
    products = Product.objects.filter(is_active=True)
    context['products'] = products
    print(products)
    return render(request, 'menu.html', context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def header(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,":",upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,'header.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid username/password!"
                return render(request,'header.html',context)
    else:
        return render(request,'header.html')

def logout_view(request):
    logout(request)
    return redirect('/home')

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    
    client = razorpay.Client(auth=("rzp_test_IUwPgd6O0ty6kF", "4tO6JU7a36QWOoJrCVyhIsCP"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    uemail=request.user.username
    context['uemail']=uemail
    return render(request,'pay.html',context)

def sendusermail(request):
    send_mail(
        "Food-Order Placed Successfully!!",
        "Order Placed. Shop with us again!",
        "ksujitha377@gmail.com",  
        ["ksujitha377@gmail.com"],  
        fail_silently=False,
    )
    context = {"message": "Order Placed!! Mail sent!"}
    return HttpResponse("Email sent successfully.") 
    

def search_results(request):
    query = request.GET.get('query')
    print("Query:", query)  # Debugging statement
    if query:
        products = Product.objects.filter(name__icontains=query)
        print("Filtered Products:", products) 
        if not products:  # If no products found
            context = {"message": "OOPS!! Product you're searching for is not available. Please search for other Menu here."}
            return render(request, 'menu.html', context)
    else:
        products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})

