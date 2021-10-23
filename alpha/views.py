from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login
from .models import Expense
from datetime import date,datetime
# Create your views here.
def v_index(request, comment=""):
    return render(request, 'index.html', {'comment' : comment } )

def v_register(request):
    if request.method == 'POST':
        ufname = request.POST['txt_firstname']
        ulname = request.POST['txt_lastname']
        passwd = request.POST['pwd_signin']
        confirm_passwd = request.POST['pwd_signin_2']
        umail = request.POST['txt_email']
        username = request.POST['txt_username']
        formdate = date.today()
        if User.objects.filter(username = username).exists():
            comment = 'Username is taken'
            return render(request,'registration/register.html', {'title': 'Sign In', 'comment': comment})
        elif User.objects.filter(email=umail).exists():
            comment = 'Email is taken'
            return render(request,'registration/register.html', {'title': 'Sign In', 'comment': comment})
        else:
            if 8 <= len(passwd) <= 12:
                if passwd == confirm_passwd:
                    usr = User(username=username, password=passwd,first_name=ufname,last_name = ulname,email=umail)
                    usr.save()
                    comment = 'Successfully signed in! Please use the login window to login now...'
                    messages.success(request, "Successfully signed in! Please use the login window to login now...")
                    return redirect("Index")
                else:
                    return render(request,'registration/register.html', {'title': 'Sign In', 'comment':'Passwords are not matching!' })
            else:
                return render(request,'registration/register.html', 
                {'title': 'Sign In', 'comment':'Passwords length is not matching! It should be within 8 to 12 characters.' })
    else:
        return render(request,'registration/register.html', {'title': 'Sign In'})


def v_login(request):
    if request.method == 'POST':
        uname = request.POST['txt_username']
        passwd = request.POST['pwd_login']
        user = authenticate(username=uname,password=passwd)
        formdate = date.today()
        if user is not None:
            if user.is_active:
                login(request,user)
                exp = Expense.objects.filter(exp_date=formdate)
                return redirect(f"/home/{str(formdate)}",{'user':user, 'exps':exp, 'appdate' : formdate})
            else:
                return render(request,'registration/login.html',{ 'comment' :'Please check your Email and Password '} )
        else:
            return render(request,'registration/login.html', {'comment' : 'User not found ! '})
    elif request.method == 'GET':
        return render(request,'registration/login.html')

def v_home(request,sdate):
    if request.method== 'GET':
        ddate=datetime.strptime(sdate,"%Y-%m-%d")
        ex = Expense.objects.filter(userid= request.user, exp_date=ddate)
        totexp=0
        for e in ex:
            totexp = totexp + e.exp_amount
        context = {'exps':ex, 'appdate':sdate , 'total':totexp, 'expone': False}
        return render(request,'Homepage.html',context)


def v_add(request,expense, amount,desc,expdate):
    mon_list = ['None','January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'] 
    dexpdate=datetime.strptime(expdate,"%Y-%m-%d")
    mon = mon_list[dexpdate.month]
    yr = dexpdate.year
    objExp=Expense(userid=request.user,exp_date=dexpdate,exp_name=expense,exp_desc=desc , exp_amount=amount , exp_month = mon,exp_year = yr )
    objExp.save()
    return redirect(f"/home/{expdate}")


def v_update(request,eid, expense, amount,desc,expdate):
    mon_list = ['None','January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'] 
    dexpdate=datetime.strptime(expdate,"%Y-%m-%d")
    mon = mon_list[dexpdate.month]
    yr = dexpdate.year
    objExp=Expense(userid=request.user,id=eid,exp_date=dexpdate,exp_name=expense,exp_desc=desc , exp_amount=amount , exp_month = mon,exp_year = yr )
    objExp.save()
    return redirect(f"/home/{expdate}")

def v_delete(request,expid,expdate):
    exp = Expense.objects.filter(id=expid)
    exp.delete()
    return redirect(f"/home/{expdate}")

def v_report(request,mon,yr):

    exps = Expense.objects.filter(userid = request.user, exp_month = mon, exp_year = yr)
    mon_dict = {'January' : '01', 'February' : '02', 'March': '03', 'April' : '04', 'May' : '05', 'June' : '06', 
    'July' : '07', 'August' : '08', 'September' : '09', 'October' : '10', 'November' : '11', 'December':'12', } 
    page_date = yr +"-" + mon_dict[mon]
    exps_o = exps.order_by('exp_date')
    exp_list = [e.exp_amount for e in exps]
    totexp = sum(exp_list)
    return render(request,'Reports.html', { 'exps' : exps_o, 'page_date': page_date , 'totexp' : totexp })

def v_find(request,p_exp_name = " "):
    if p_exp_name == " ":
        exps="Empty"
        return render(request,"findexp.html", { 'exps' : exps })
    exps = Expense.objects.filter(userid = request.user, exp_name = p_exp_name)
    if exps.count() == 0:
        exps = "Not Found"
        return render(request,"findexp.html", { 'exps' : exps })
    return render(request,"findexp.html", { 'exps' : exps })

def v_logout(request):
    auth.logout(request)
    return redirect("Index")