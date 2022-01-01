from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login
from .models import Expense, UserImage, Income
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
            comment = 'Username is taken! Please choose a different username !'
            return render(request,'register/register.html', {'title': 'Sign In', 'comment': comment})
        elif User.objects.filter(email=umail).exists():
            comment = 'Email is taken! Please check the email once again or login with the current email'
            return render(request,'register/register.html', {'title': 'Sign In', 'comment': comment})
        else:
            if 8 <= len(passwd) <= 12:
                if passwd == confirm_passwd:
                    usr = User(username=username, password=passwd,first_name=ufname,last_name = ulname,email=umail)
                    usr.save()
                    comment = 'Successfully signed in! Please use the login window to login now...'
                    messages.success(request, "Successfully signed in! Please use the login window to login now...")
                    return redirect("Index")
                else:
                    return render(request,'register/register.html', {'title': 'Sign In', 'comment':'Passwords are not matching!' })
            else:
                return render(request,'register/register.html', 
                {'title': 'Sign In', 'comment':'Passwords length is not matching! It should be within 8 to 12 characters.' })
    else:
        return render(request,'register/register.html', {'title': 'Sign In'})


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
                return render(request,'register/login.html',{ 'comment' :'Please check your Uesrname and Password '} )
        else:
            return render(request,'register/login.html', {'comment' : 'User not found ! '})
    elif request.method == 'GET':
        return render(request,'register/login.html')

def v_home(request,sdate):
    if request.method== 'GET':
        ddate=datetime.strptime(sdate,"%Y-%m-%d")
        
        ex = Expense.objects.filter(userid= request.user, exp_date=ddate)
        totexp=sum( [e.exp_amount for e in ex ] )

        inc = Income.objects.filter(userid = request.user, inc_date=ddate)
        totinc = sum( [i.inc_amount for i in inc] )
        
        context = {'exps':ex,  'incs': inc, 'appdate':sdate , 'totexp':totexp, 'totinc':totinc ,'expone': False}
        return render(request,'Homepage.html',context)

def v_profile(request):
    if request.method=='GET':
        return render(request, "profile.html")
    elif request.method == 'POST':
        my_user = User.objects.filter(id=request.user.id)
        my_user = my_user[0]

        my_profile_pic = UserImage.objects.filter(id=my_user.id)
        u_img = request.POST.get('profile_pic')
        my_user.first_name = request.POST.get('txt_ufname', my_user.first_name)
        my_user.last_name = request.POST.get('txt_ulname', my_user.last_name)
        my_user.username = request.POST.get('txt_username', my_user.username )
        my_user.email = request.POST.get('txt_email',my_user.email )

        my_user.save()

        if my_profile_pic :
            my_profile_pic = my_profile_pic[0]
            my_profile_pic.userimage = u_img
            my_profile_pic.save()
        else:
            user_pro_pic = UserImage(userid=my_user, userimage=u_img)
            user_pro_pic.save()

        text = {'my_user': my_user, 'cmt': 'All working fine !'}
        return render(request, "profile.html", text )
    else:
        usr_img = UserImage.objects.filter(userid=request.user.id)
        if usr_img:
            propic = usr_img[0]
        else:
            propic = 'imgs/default.jpg'

        return render(request, "profle.html",  {'cmt': 'Unknown Method', 'user_img' : propic} )


def v_add(request,expense, amount,desc,expdate):
    mon_list = ['None','Jauary', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'] 
    dexpdate=datetime.strptime(expdate,"%Y-%m-%d")
    mon = mon_list[dexpdate.month]
    yr = dexpdate.year
    objExp=Expense(userid=request.user,exp_date=dexpdate,exp_name=expense,exp_desc=desc , exp_amount=amount , exp_month = mon,exp_year = yr )
    objExp.save()
    return redirect(f"/home/{expdate}")

def v_add_inc(request,inc, amount,desc,incdate):
    mon_list = ['None','Jauary', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'] 
    dincdate=datetime.strptime(incdate,"%Y-%m-%d")
    mon = mon_list[dincdate.month]
    yr = dincdate.year
    objInc=Income(userid=request.user,inc_date=dincdate,inc_name=inc,inc_desc=desc , inc_amount=amount , inc_month = mon,inc_year = yr )
    objInc.save()
    return redirect(f"/home/{incdate}")


def v_update(request,eid, expense, amount,desc,expdate):
    mon_list = ['None','January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'] 
    dexpdate=datetime.strptime(expdate,"%Y-%m-%d")
    mon = mon_list[dexpdate.month]
    yr = dexpdate.year
    objExp=Expense(userid=request.user,id=eid,exp_date=dexpdate,exp_name=expense,exp_desc=desc , exp_amount=amount , exp_month = mon,exp_year = yr )
    objExp.save()
    return redirect(f"/home/{expdate}")


def v_update_inc(request,iid, inc, amount,desc,incdate):
    mon_list = ['None','January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'] 
    dincdate=datetime.strptime(incdate,"%Y-%m-%d")
    mon = mon_list[dincdate.month]
    yr = dincdate.year
    objInc=Income(userid=request.user,id=iid,inc_date=dincdate,inc_name=inc,inc_desc=desc , inc_amount=amount , inc_month = mon,inc_year = yr )
    objInc.save()
    return redirect(f"/home/{incdate}")


def v_delete(request,expid,expdate):
    exp = Expense.objects.filter(id=expid)
    exp.delete()
    return redirect(f"/home/{expdate}")


def v_delete_inc(request,incid,incdate):
    inc = Income.objects.filter(id=incid)
    inc.delete()
    return redirect(f"/home/{incdate}")


def v_report(request,mon,yr):
    exps = Expense.objects.filter(userid = request.user, exp_month = mon, exp_year = yr)
    incs = Income.objects.filter(userid = request.user, inc_month = mon, inc_year = yr)
    mon_dict = {'January' : '01', 'February' : '02', 'March': '03', 'April' : '04', 'May' : '05', 'June' : '06', 
    'July' : '07', 'August' : '08', 'September' : '09', 'October' : '10', 'November' : '11', 'December':'12', } 
    page_date = yr +"-" + mon_dict[mon]
    exps_o = exps.order_by('exp_date')
    incs_o = incs.order_by('inc_date')
    exp_list = [e.exp_amount for e in exps]
    inc_list = [i.inc_amount for i in incs]
    totexp = sum(exp_list)
    totinc = sum(inc_list)
    vals = {    'exps' : exps_o, 'totexp' : totexp, 'page_date': page_date ,
                'incs' : incs_o, 'totinc' : totinc }
    return render(request,'Reports.html', vals)

def v_find(request,p_txn_name = " "):
    if p_txn_name == " ":
        txn_cmt="Empty"
        return render(request,"findexp.html", { 'txn_cmt' : txn_cmt })
    exps = Expense.objects.filter(userid = request.user, exp_name = p_txn_name)           
    incs = Income.objects.filter(userid = request.user, inc_name = p_txn_name)
    txns = list(exps) + list(incs)
    
    if len(txns) ==0 :
        txt_cmt = "404"
        return render(request,"findexp.html", { 'txn_cmt' : txt_cmt })    
    else:
        if incs.count() !=0 and exps.count() !=0 :    
            return render(request,"findexp.html", { 'incs' : incs , 'exps' : exps, 'txn_cmt' : '200' }) 
        elif incs.count() == 0 and exps.count() !=0:
            return render(request,"findexp.html", { 'exps' : exps , 'txn_cmt' : '200'})
        elif exps.count() == 0 and incs.count() !=0:
            return render(request,"findexp.html", { 'incs' : incs , 'txn_cmt' : '200' })       
        return render(request,"findexp.html", { 'txn_cmt' : '404' })    

def v_logout(request):
    auth.logout(request)
    return redirect("Index")