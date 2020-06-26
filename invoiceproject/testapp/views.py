from django.shortcuts import render,redirect
from django.template import Context
from django.template.loader import get_template
from io import StringIO,BytesIO
from xhtml2pdf import pisa
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import UserSignup
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.
from random import choice
def invid_gen():
    no = [0,1,2,3,4,5,6,7,8,9]
    hc = ['A','B','C','D','E','F']
    return str(choice(no)) + choice(hc) + str(choice(no)) + choice(hc) + str(choice(no)) + choice   (hc) + str(choice(no)) + choice(hc)
def amount_gen(s):
    s1 = 0
    for i in s:
        s1 += ord(i)
    return s1
@login_required(login_url = "/login/")
def home(request):
    return render(request,"home.html")
def signup_view(request):
    if request.method == "POST":
        pwd1 = request.POST["pwd1"]
        pwd2 = request.POST["pwd2"]
        username = request.POST["username"]
        fullname = request.POST["fullname"]
        email = request.POST["email"]
        phn = request.POST['phn']
        if pwd1 == pwd2 and len(pwd1) >= 5:
            try:
                user = User.objects.get(username=username)
                d = {"pdm":"Username already taken..."}
                return render(request,'signup.html',d)
            except User.DoesNotExist:
                user= User.objects.create_user(username=username,password=pwd1)
                UserSignup(user=user,fullname=fullname,email=email,phn=phn).save()
                login(request,user)
                data = UserSignup.objects.get(user=user)
                request.session["fullname"] = data.fullname
                request.session['email'] = data.email
                request.session["phn"] = data.phn
                return redirect("/")
        else:
            d = {"pdm":"password must be matched and password must contain at least 5 charcters"}
            return render(request,'signup.html',d)
    else:
        return render(request,'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        pwd = request.POST["pwd"]
        user = authenticate(username=username,password=pwd)
        if user is not None:
            login(request,user)
            data = UserSignup.objects.get(user=user)
            request.session["fullname"] = data.fullname
            request.session['email'] = data.email
            request.session["phn"] = data.phn
            return redirect("/")
        else:
            d = {"pdm":"Invalid Username and Password"}
            return render(request,'login.html',d)
    else:
        return render(request,'login.html')
@login_required(login_url="/login/")
def invoice_view(request):
    name = request.session['fullname']
    email = request.session['email']
    phn = request.session['phn']
    amount = amount_gen(name)
    invid = invid_gen()
    data = {"name":name,"invid":invid,"amount":amount,"email":email,"phn":phn}
    template = get_template("invoice.html")
    data_p = template.render(data)
    response = BytesIO()
    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type = "application/pdf")
    else:
        return HttpResponse("Error Generating PDF")
    return render(request,'invoice.html',data)

def logout_view(request):
    del request.session['fullname']
    del request.session['email']
    del request.session['phn']
    logout(request)
    return redirect("/")