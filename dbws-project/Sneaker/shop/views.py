from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from django.db.models import Count,Max
from .form import LoginForm,RegisterForm
from .models import buyer,sneaker,seller,sold,inventory,customization
from .models import order as orders
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.

def login(request):
    if request.session.get('is_login',None):# If is_login return index
        return redirect('/sneaker/index')
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "Please check !"
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            type = login_form.cleaned_data.get("type")
            if type=='b':# Verify character
                try:
                    u = buyer.objects.get(username=username)
                    if u.password == password:# Create session
                        request.session['is_login']=True
                        request.session['user_id']=u.id
                        request.session['user_name']=u.username
                        request.session['user_type']=type
                        return redirect('/sneaker/index')
                    else:
                        message = "Wrong password !"
                except:
                    message = "User doesn't exist !"
            if type=='s':
                try:
                    u = seller.objects.get(username=username)
                    if u.password == password:
                        request.session['is_login']=True
                        request.session['user_id']=u.id
                        request.session['user_name']=u.username
                        request.session['user_type'] = type
                        return redirect('/sneaker/index')
                    else:
                        message = "Wrong password !"
                except:
                    message = "User doesn't exist !"
        return render(request, 'login/login.html', locals())

    login_form = LoginForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect("/sneaker/index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check !"
        if register_form.is_valid():# Check user
                    username = register_form.cleaned_data.get("username")
                    password1 = register_form.cleaned_data.get("password1")
                    password2 = register_form.cleaned_data.get("password2")
                    address=register_form.cleaned_data.get("address")
                    type=register_form.cleaned_data.get("type")
                    if type=='b':# Verify character
                        if password1 != password2:
                            message = "Passwords are not same !"
                            return render(request, 'login/register.html', locals())
                        else:
                            same_name_user = buyer.objects.filter(username=username)
                            if same_name_user:
                                message = 'User exist !'
                                return render(request, 'login/register.html', locals())
                            new_user = buyer.objects.create()# Create an account
                            new_user.username = username
                            new_user.password = password1
                            new_user.address=address
                            new_user.save()
                            return redirect('/sneaker/login')
                    if type == 's':
                        if password1 != password2:
                            message = "Passwords are not same !"
                            return render(request, 'login/register.html', locals())
                        else:
                            same_name_user = seller.objects.filter(username=username)
                            if same_name_user:
                                message = 'User exist !'
                                return render(request, 'login/register.html', locals())
                            new_user = seller.objects.create()
                            new_user.username = username
                            new_user.password = password1
                            new_user.address = address
                            new_user.save()
                            return redirect('/sneaker/login')
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

def index(request):
    brands = sneaker.objects.values("brand").annotate(counts=Count("brand"))
    if request.GET.get('searchkey'):# Search
        key = request.GET.get('searchkey')
        s = sneaker.objects.filter(name__icontains=key)
        paginator = Paginator(s, 12)
        page = request.GET.get('page')
        try:# Paginator
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except InvalidPage:
            message = 'Cannot find'
            return render(request, "notice.html", locals())
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)
        return render(request, 'library.html', {'objs': objs, 'p2': objs.number + 1, 'p3': objs.number + 2})
    elif request.GET.get('brand'):
        s = sneaker.objects.filter(brand=request.GET.get('brand'))
        paginator = Paginator(s, 12)
        page = request.GET.get('page')
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except InvalidPage:
            message = 'Cannot find'
            return render(request, "notice.html", locals())
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)
        return render(request, 'library.html', {'objs': objs, 'p2': objs.number + 1, 'p3': objs.number + 2})
    objs=sneaker.objects.all()[:6]
    return render(request,'index.html',{'objs':objs,"brands":brands})

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/sneaker/index')
    request.session.flush()#Clear session
    return redirect('/sneaker/index')

def library(request):
    if request.method=='GET':
        mywhere=[]
        brand=request.GET.get('brand')
        searchkey=request.GET.get('searchkey')
        page = request.GET.get('page')
        brands=sneaker.objects.values("brand").annotate(counts=Count("brand"))
        s = sneaker.objects.all()
        if searchkey:# Keep search and filter to paginator
            s = s.filter(name__icontains=searchkey)
            mywhere.append("searchkey="+searchkey)
            paginator = Paginator(s, 12)
        if brand:
            s=s.filter(brand=request.GET.get('brand'))
            mywhere.append("brand=" + brand)
            paginator = Paginator(s, 12)
        else:
            paginator = Paginator(s, 12)

        try:
            objs=paginator.page(page)
        except PageNotAnInteger:
            objs=paginator.page(1)
        except InvalidPage:
            message = 'Cannot find'
            return render(request, "notice.html", locals())
        except EmptyPage:
            objs=paginator.page(paginator.num_pages)
        p2= objs.number + 1
        p3= objs.number + 2
    return render(request, 'library.html',locals())

def item(request):
    if request.method == 'GET':
        id=request.GET.get('id')
        item=sneaker.objects.get(id=id)
        inv=inventory.objects.filter(sneakerid=id).count()# Total amount
        return render(request,'item.html',{'item':item,'inv':inv})
    if request.method=='POST':
        id = request.GET.get('id')
        if inventory.objects.filter(sneakerid_id=id).count()!=0:
            custom=request.POST.get('custom')
            sneakerid = request.POST.get('sneakerid')
            buyed=inventory.objects.filter(sneakerid_id=sneakerid)
            if request.session.get('is_login',None):
                new_order=orders.objects.create(inventoryid_id=buyed[0].id,
                                                buyer_id=request.session['user_name'],
                                                seller_id=buyed[0].seller_id)
                new_sold=sold.objects.create(soldid=new_order.inventoryid_id,sneakerid_id=sneakerid)
                if custom!='null':
                    new_customization=customization.objects.create(color=custom)
                    new_customization.save()
                    new_order.custom_id=new_customization.id
                else:
                    new_order.custom_id = None
                new_order.save()
                new_sold.save()
                buyed[0].delete()# Save and delete
                message = 'Success Buy'
                return render(request, "notice.html", locals())
            else:
                return redirect('/sneaker/login')
        else:return redirect('/sneaker/index')

def order(request):
    if request.session.get('is_login',None):
        if request.session['user_type']=='b':
            ret = []
            o = orders.objects.filter(buyer=request.session['user_name'])
            if (len(o) != 0):
                for item in o:
                    tmp_dict = {}
                    print(item.custom)
                    tmp_dict['order_id'] = item.id# Join the table and select
                    tmp_dict['sneaker_id'] = item.inventoryid_id
                    tmp_dict['buyer'] = item.buyer_id
                    tmp_dict['time'] = item.c_time
                    tmp_dict['custom_id'] = item.custom
                    tmp_dict['seller']=item.seller_id
                    if tmp_dict['custom_id']:
                        cc=customization.objects.get(id=item.custom_id)
                        tmp_dict['custom']=cc.color
                    else:
                        tmp_dict['custom'] ='NULL'
                    ins = sold.objects.filter(soldid=tmp_dict['sneaker_id'])
                    type_id = ins[0].sneakerid_id
                    s=sneaker.objects.filter(id=type_id)[0]
                    if s:
                        tmp_dict['sneaker_name'] = s.name
                    else:
                        tmp_dict['sneaker_name'] = 'unknown'
                    ret.append(tmp_dict)
        if request.session['user_type'] == 's':
            ret = []
            o = orders.objects.filter(seller=request.session['user_name'])
            if (len(o) != 0):
                for item in o:
                    tmp_dict = {}
                    print(item.id)# Join the table and select
                    tmp_dict['order_id'] = item.id
                    tmp_dict['sneaker_id'] = item.inventoryid_id
                    tmp_dict['buyer'] = item.buyer_id
                    tmp_dict['time'] = item.c_time
                    tmp_dict['custom_id'] = item.custom
                    tmp_dict['seller'] = item.seller_id
                    if tmp_dict['custom_id']:
                        cc=customization.objects.get(id=item.custom_id)
                        tmp_dict['custom']=cc.color
                    else:
                        tmp_dict['custom'] ='NULL'
                    ins = sold.objects.filter(soldid=tmp_dict['sneaker_id'])
                    type_id = ins[0].sneakerid_id
                    s = sneaker.objects.filter(id=type_id)[0]

                    if s:
                        tmp_dict['sneaker_name'] = s.name
                    else:
                        tmp_dict['sneaker_name'] = 'unknown'
                    ret.append(tmp_dict)
        paginator = Paginator(ret, 12)
        if request.method == 'GET':
            page = request.GET.get('page')# Paginator
            try:
                objs = paginator.page(page)
            except PageNotAnInteger:
                objs = paginator.page(1)
            except InvalidPage:
                message = 'Cannot find'
                return render(request, "notice.html", locals())
            except EmptyPage:
                objs = paginator.page(paginator.num_pages)
        return render(request, 'order.html', {'objs': objs, 'p2': objs.number + 1, 'p3': objs.number + 2})
    return redirect('/sneaker/login')

def sell(request):
    if request.session.get('is_login', None):
        if request.method=='GET':
            mywhere=[]
            searchkey = request.GET.get('searchkey')
            s = sneaker.objects.all()
            if searchkey:
                s=s.filter(name__icontains=searchkey)
                mywhere.append("searchkey=" + searchkey)
                paginator = Paginator(s, 12)
            else:
                paginator = Paginator(s, 12)
            page=request.GET.get('page')
            try:
                objs=paginator.page(page)
            except PageNotAnInteger:
                objs=paginator.page(1)
            except InvalidPage:
                message = 'Cannot find'
                return render(request, "notice.html", locals())
            except EmptyPage:
                objs=paginator.page(paginator.num_pages)
            p2 = objs.number + 1
            p3 = objs.number + 2
            return render(request,'sell.html',locals())
        if request.method=='POST':
            if request.POST.get('sellid'):
                id=request.POST.get('sellid')# Create a table
                inventorymax=inventory.objects.aggregate(max=Max("id"))['max']
                soldmax=sold.objects.aggregate(max=Max("soldid"))['max']
                print(inventorymax)
                print(soldmax)
                if inventorymax>soldmax:
                    newid=inventorymax+1
                else:
                    newid=soldmax+1
                newinventory=inventory.objects.create(id=newid,seller_id=request.session['user_name'],sneakerid_id=id)
                print(newinventory)
                newinventory.save()
                message='Success Sell'
                return render(request,"notice.html",locals())
            else:
                message = 'Fail'
                return render(request, "notice.html", locals())
        return render(request,'sell.html')
    return redirect('/sneaker/login')

def sell_order(request):
    if request.session.get('is_login',None):
        i = inventory.objects.filter(seller_id=request.session['user_name'])
        if (len(i) != 0):
            ret=[]
            for item in i:
                tmp_dict = {}# Join table and select
                tmp_dict['id'] = item.id
                tmp_dict['sneaker_id'] = item.sneakerid_id
                tmp_dict['seller']=item.seller_id
                ins = sneaker.objects.get(id=tmp_dict['sneaker_id'])
                tmp_dict['sneaker_name']=ins.name
                tmp_dict['price']=ins.price
                tmp_dict['brand'] = ins.brand
                ret.append(tmp_dict)
            paginator = Paginator(ret, 12)
            print(ret)
            if request.method == 'GET':
                page = request.GET.get('page')
                try:
                    objs = paginator.page(page)
                except PageNotAnInteger:
                    objs = paginator.page(1)
                except InvalidPage:
                    message = 'Cannot find'
                    return render(request, "notice.html", locals())
                except EmptyPage:
                    objs = paginator.page(paginator.num_pages)
                p2= objs.number + 1
                p3= objs.number + 2
            return render(request, 'sell_order.html', locals())
        return render(request,'sell_order.html')
    return redirect('/sneaker/login')

def info(request):
    if request.method=='GET':
        if request.session['user_type']=='s':
            address=seller.objects.get(id= request.session['user_id']).address# get address before
        if request.session['user_type']=='b':
            address=buyer.objects.get(id= request.session['user_id']).address
        return render(request, 'info.html', locals())
    if request.method=='POST':
        if request.POST.get('newaddress'):# Change address
            if request.session['user_type'] == 's':
                user = seller.objects.get(id=request.session['user_id'])
                user.address=request.POST.get('newaddress')
                user.save()
            if request.session['user_type'] == 'b':
                user = buyer.objects.get(id=request.session['user_id'])
                user.address = request.POST.get('newaddress')
                user.save()
            return redirect('/sneaker/info')
        if request.POST.get('password1') and request.POST.get('password2'):
            po=request.POST.get('passwordold')
            p1=request.POST.get('password1')
            p2=request.POST.get('password2')#Check user
            if request.session['user_type'] == 's':
                if seller.objects.filter(password=po):
                    if p1==p2:
                        user = seller.objects.get(id=request.session['user_id'])
                        user.password = p1
                        user.save()
                        message='success'
                    else:
                        message = "Password not same!"
                else:
                    message="Wrong old password"
            if request.session['user_type'] == 'b':
                if buyer.objects.filter(password=po):
                    if p1 == p2:
                        user = buyer.objects.get(id=request.session['user_id'])
                        user.password = p1
                        user.save()
                        message = 'success'
                    else:
                        message = "Password not same!"
                else:
                    message="Wrong old password"
        else:
            message="Check enter!"
    return render(request, 'info.html',locals())