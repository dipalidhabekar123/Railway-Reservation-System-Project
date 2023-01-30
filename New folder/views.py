from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages

# Create your views here.
def nav(request):
    return render(request,'carousel.html')


def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')


def Login_customer(request):
    error = False
    error2 = False
    error3 = False
    if request.method == "POST":
        n = request.POST['uname']
        p = request.POST['pwd']
        try:
            user = authenticate(username=n,password=p)
        except:
            error3 = True
        try:

            if user.is_staff:
                login(request,user)
                error2 = True
            elif user:
                login(request, user)
                error=True
        except:
            error3=True



    d = {'error':error,'error2':error2,'error3':error3}
    return render(request,'login_customer.html',d)

def Register_customer(request):
    error = False
    if request.method == "POST":
        n = request.POST['uname']
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        a = request.POST['add']
        m = request.POST['mobile']
        g = request.POST['male']
        d = request.POST['birth']
        p = request.POST['pwd']
        user = User.objects.create_user(first_name=f,last_name=l,username=n,password=p,email=e)
        Register.objects.create(user=user,add=a,mobile=m,gender=g,dob=d)
        error = True
    d = {'error':error}
    return render(request,'register_customer.html',d)

def Search_Train(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Add_route.objects.values('route').distinct()
    ase = Asehi.objects.all()
    coun = 0
    error=False
    fare3=0
    count = 0
    count1 = 0
    data1=0
    data2=0
    route1=[]
    route=0
    b_no =[]
    b_no1 =[]
    bhu=0
    if request.method=="POST":
        f = request.POST["fcity"]
        t = request.POST["tcity"]
        da = request.POST["date"]
        data1 = Add_route.objects.filter(route=f)
        data2 = Add_route.objects.filter(route=t)
        for i in data1:
            for j in data2:
                if i.train.train_no==j.train.train_no:
                    route1.append(Add_Train.objects.filter(train_no=i.train.train_no))
        for i in data1:
            fare1=i.fare
            count+=1
            b_no.append(i.train.train_no)
        for i in data2:
            fare2 = i.fare
            count1+=1
            b_no1.append(i.train.train_no)

        fare3 = fare2-fare1
        if fare3<5 and fare3>0:
            fare3 = 5
        elif fare3<0:
            fare3 = fare3*(-1)
        elif fare3==0:
            fare3 = fare3
        route = f+" to "+t
        Asehi.objects.create(fare=fare3,train_name="bus2",date3=da)
        for i in ase:
            coun = coun + 1
            error=True

    d={"data2":data,'route1':route1,'fare3':fare3,"error":error,'coun':coun,'route':route}
    return render(request,'search_train.html',d)


def Dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'dashboard.html')

def Logout(request):
    logout(request)
    return redirect('nav')

def Book_detail(request,coun,pid,route1):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False

    try:
        data = Asehi.objects.get(id=coun)
    except:
        data = None
    data2 = Add_Train.objects.get(id=pid)
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Passenger.objects.filter(user=user1)
    book = Book_ticket.objects.filter(user=user1)
    total = 0
    for i in pro:
        if i.status!="set":
            total = total + i.fare
    passenger=0

    if request.method=="POST":
        f = request.POST["name"]
        t = request.POST["age"]
        da = request.POST["gender"]
        passenger = Passenger.objects.create(user=user1,train=data2,route=route1,name=f,gender=da,age=t,fare=data.fare,date1=data.date3)
        Book_ticket.objects.create(user=user1, route=route1, fare=total, passenger=passenger, date2=data.date3)

        if passenger:
            error = True
    d = {'data':data,'data2':data2,'pro':pro,'total':total,'book':book,'error':error,'route1':route1,'coun':coun,'pid':pid}
    return render(request,'book_detail.html',d)

def Delete_passenger(request,pid,bid,route1):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Passenger.objects.get(id=pid)
    data.delete()
    ase = Asehi.objects.all()
    coun = 7
    for i in ase:
        coun = coun + 1
    messages.info(request,'Passenger Deleted Successfully')
    return redirect('book_detail', coun,bid,route1)

def Card_Detail(request,total,coun,route1,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    try:
        data = Asehi.objects.get(id=coun)
    except:
        data=None
    data2 = Add_Train.objects.get(id=pid)
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Passenger.objects.filter(user=user1)
    book = Book_ticket.objects.filter(user=user1)
    count=0
    pro1 = 0
    if request.method == "POST":
        error=True
        for i in pro:
            count = i.name
            if i.status != "set":
                i.status="set"
                i.save()
        return redirect('my_booking')

    total1=total
    d = {'user':user1,'data':data,'data2':data2,'pro':pro,'pro1':pro1,'total':total1,'book':book,'error':error,'route1':route1,'count':count}
    return render(request,'card_detail.html',d)


def my_booking(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Passenger.objects.filter(user=user1)
    book = Book_ticket.objects.filter(user=user1)
    d = {'user':user1,'pro':pro,'book':book}
    return render(request,'my_booking.html',d)


def view_ticket(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    book = Book_ticket.objects.get(id=pid)
    d = {'book':book}
    return render(request,'view_ticket.html',d)


def viewbookings(request):
    if not request.user.is_authenticated:
        return redirect('login')
    book = Book_ticket.objects.all()
    d = {'book': book}
    return render(request, 'viewbookings.html', d)


def delte_my_booking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    pro = Passenger.objects.get(id=pid)
    pro.delete()
    error=True
    d = {'error':error}
    return render(request,'my_booking.html',d)

def deletebooking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    pro = Passenger.objects.get(id=pid)
    pro.delete()
    error=True
    d = {'error':error}
    return render(request,'viewbookings.html',d)



def Add_train(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    if request.method == "POST":
        n = request.POST['busname']
        no = request.POST['bus_no']
        f = request.POST['fcity']
        to= request.POST['tcity']
        de= request.POST['dtime']
        a = request.POST['atime']
        t = request.POST['ttime']
        d = request.POST['dis']
        i = request.FILES['img']
        Add_Train.objects.create(trainname=n,train_no=no,from_city=f,to_city=to,departuretime=de,arrivaltime=a,trevaltime=t,distance=d,img=i)
        error=True
    d={"error":error}
    return render(request,'add_train.html',d)
def view_train(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Add_Train.objects.all()
    d={"data":data}
    return render(request,"view_train.html",d)
def add_route(request):
    error=False
    data=Add_Train.objects.all()

    if request.method == "POST":
        b = request.POST['bus']
        r = request.POST['route']
        f= request.POST['fare']
        d = request.POST['dis']

        bus1 = Add_Train.objects.filter(id=b).get()
        Add_route.objects.create(train=bus1,route=r,distance=d,fare=f)
        error = True

    d={"data":data,"error":error}

    return render(request,'add_route.html',d)

def Edit_route(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    data=Add_route.objects.get(id=pid)
    data2=Add_Train.objects.all()

    if request.method == "POST":
        b = request.POST['bus']
        r = request.POST['route']
        f= request.POST['fare']
        d = request.POST['dis']

        a = Add_Train.objects.filter(id=b).first()
        data.train = a
        data.route = r
        data.fare = f
        data.distance = d
        data.save()
        error=True

    d={"data":data,"data2":data2,"error":error}
    return render(request,'editroute.html',d)


def edit(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    data1=Add_Train.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['busname']
        no = request.POST['bus_no']
        de= request.POST['dtime']
        a = request.POST['atime']
        t = request.POST['ttime']
        f = request.POST['fcity']
        to= request.POST['tcity']
        d = request.POST['dis']
        data1.trainname=n
        data1.train_no=no
        data1.from_city=f
        data1.to_city=to
        data1.departuretime=de
        data1.arrivaltime=a
        data1.traveltime=t
        data1.distance=d
        data1.save()
        error = True
    d = {'data':data1,'error':error}
    return render(request,'edittrain.html',d)

def delete(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error2=False
    data=Add_Train.objects.get(id=pid)
    data.delete()
    error2=True
    d = {'error2':error2}
    return render(request,"view_train.html",d)


def delete_route(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    data=Add_route.objects.get(id=pid)
    data.delete()
    error = True
    d = {'error2':error}
    return render(request,"availableroute.html",d)

def displayroute(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Add_route.objects.all()
    data2 = Add_Train.objects.all()
    d = {'data':data,'data2':data2}
    return render(request,"availableroute.html",d)

def admindashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'admindashboard.html')

def change_image(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    train = Add_Train.objects.get(id=pid)
    error = ""
    if request.method=="POST":
        try:
            i = request.FILES['newpic']
            train.img = i
            train.save()
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'train':train}
    return render(request, 'change_image.html', d)



def view_regusers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Register.objects.filter(user__is_staff=False)
    d={"data":data}
    return render(request,"view_regusers.html",d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_regusers')