from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .filters import *
#login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
#custom decorator
from .decorators import *
#group management
from django.contrib.auth.models import Group
from Tracker.models import Profile
# Create your views here.

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('info')
        else:
            messages.info(request,'Userrname or Password is Incorrect')
            return redirect('login')
    context={}
    return render(request,'Tracker/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def signup(request):
    form=CreateUserform()
    if request.method=='POST':
        form=CreateUserform(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"User Created Successfully for "+username)
            '''Add group while register bew=low two lines'''
            group= Group.objects.get(name='student')
            user.groups.add(group)
            '''Till herer'''
            '''Auto create a profile of a user'''
            Profile.objects.create(user=user)
            '''Till here'''
            return redirect('login')
    context={
            'form':form
        }
    return render(request,'Tracker/signup.html',context)


    
@login_required(login_url='login')
def userpage(request):
    information=request.user.profile
    context={
        'info':information
    }
    return render(request,'Tracker/userpage.html',context)    

@login_required(login_url='login')
def profile(request,pk):
    profile_info=Profile.objects.get(id=pk)
    context={
        'info':profile_info,
    }
    return render(request,'Tracker/profile.html',context)

@login_required(login_url='login')
def info(request):
    #pdata is personal data
    data=Profile.objects.all()
    for i in data:
        if i.RollNo is None and not request.user.is_staff:
            messages.success(request,"Please Fill Out the Known Information")
            return redirect('/cruds/'+str(i.id))
    search=ProfileFilter(request.GET,queryset=data)
    data=search.qs
    context={
        'data':data,
        'search':search,
    }
    return render(request,'Tracker/info.html',context)

#Create and Update = CRUD
#Without giving instace and pk it will work as a create method and add new profile to database
@login_required(login_url='login')
def crud(request,pk):
    profile_info=Profile.objects.get(id=pk)
    form=ProfileForm(instance=profile_info)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile_info)
        if form.is_valid():
            form.save()
        return redirect('info')
    context={
        'form':form
        }
    return render(request,'Tracker/createupdate.html',context)

@login_required(login_url='login')
def deleteprofile(request,pk):
    profile_info=Profile.objects.get(id=pk)
    profile_info.delete()
    return redirect('info')

@login_required(login_url='login')
@admin_only
def dashboard(request):
    return render(request,'Tracker/dashboard.html')

    