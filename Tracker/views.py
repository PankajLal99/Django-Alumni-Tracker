from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .filters import *
import time
#login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
#custom decorator
from .decorators import *
#group management
from django.contrib.auth.models import Group
from Tracker.models import Profile
# Scrapping Import
from .scraper import linkedIn
# charts
import pandas as pd
import plotly.express as px
import chart_studio.plotly as py
import plotly.offline as opy
import csv 
from pandas import DataFrame as df
from datetime import datetime
from datetime import date
from django.core.paginator import Paginator
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
            '''Add group while register bewlow two lines'''
            group= Group.objects.get(name='student')
            user.groups.add(group)
            '''Till herer''' 
            '''Auto create a profile of a user'''
            newpro=Profile.objects.create(user=user)
            Scrapper_Data.objects.create(profile=newpro)
            '''Till here'''
            return redirect('login')
    context={
            'form':form
        }
    return render(request,'Tracker/signup.html',context)


    
@login_required(login_url='login')
def userpage(request):
    information=request.user.profile
    data=Scrapper_Data.objects.get(profile=information)
    context={
        'info':information,
        'data':data,
    }
    return render(request,'Tracker/userpage.html',context)    

@login_required(login_url='login')
def profile(request,pk):
    profile_info=Profile.objects.get(id=pk)
    data=Scrapper_Data.objects.get(profile=profile_info)
    context={
        'info':profile_info,
        'data':data,
    }
    return render(request,'Tracker/profile.html',context)

@login_required(login_url='login')
def info(request):
    blog=Blog.objects.filter(status=1).order_by('-created_on')[0:3]
    #orm
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
        'blogs':blog,
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
def scrapper(request):
    obj = linkedIn()
    l=Profile.objects.all()
    try:
        obj.login()
        for i in l:
            data=obj.scrap(i.linkedIn_Link)
            Scrapper_Data.objects.filter(profile=i).update(name=data[1],profile_title=data[2],location=data[3],connection=data[4],   experience=data[7],job_title=data[5],joining_date=data[6],college_name=data[8],degree_name=data[9],stream=data[10],degree_year=data[11])
            time.sleep(5)
        obj.close()
        return HttpResponse('True')
    except:
        obj.close()
        return HttpResponse('False')
    

@login_required(login_url='login')
def post(request):
    if request.method=='POST':
        if not request.user.is_staff:
            title= request.POST.get('title','')
            content= request.POST.get('content','')
            img= request.FILES.get('image','static/images/bg.jpg')
            Blog.objects.create(title=title,content=content,image=img,author=request.user)
            messages.warning(request,"Your Request Has been Sent !! ")
            return redirect('info')
        else:
            title= request.POST.get('title','')
            content= request.POST.get('content','')
            img= request.FILES.get('image','static/images/bg.jpg')
            Blog.objects.create(title=title,content=content,image=img,status=1)
            return redirect('dashboard')
    return render(request,'Tracker/post.html')

@login_required(login_url='login')
def blog(request):
    data=Blog.objects.filter(status=1).order_by('-created_on')
    context={
        'blogs':data
    }
    return render(request,'Tracker/blogs.html',context)
@login_required(login_url='login')
def showblog(request,pk):
    data=Blog.objects.get(id=pk)
    context={
        'blog':data,
    }
    return render(request,'Tracker/showblog.html',context)

def allowblog(request):
    data=Blog.objects.filter(status=0)
    if request.method == 'POST':
        title=request.POST['title']
        Blog.objects.filter(title=title).update(status=1)
        return redirect('blog')
    context={
        'blogs':data,
    }
    return render(request,'Tracker/allowblog.html',context)


# ############################***************************************##########################################********************************************* #


@login_required(login_url='login')
@admin_only
def dashboard(request):
        
    df = pd.DataFrame(columns=['Name','Count'])

    # fetching all the valuesv of names from the 
    
    val = Profile.objects.values('Company')
    l=[]
    
    
    # loop for putting all the name into list
    for i in val:
        l.append(i['Company'])

    
    #to get the distinct value conerted to set
    s=set(l)
    
    comp = len(s)
    for i in s:
        #filtering and fetching the count of same name and putting it in dataframe    
        d=Profile.objects.filter(Company=i)
        df=df.append({'Name':i,'Count':len(d)},ignore_index=True)
        
        
    

    fig = px.pie(df, values='Count', names='Name',color_discrete_sequence=px.colors.qualitative.Dark24,title='Companies')
    fig.update_traces(textposition='inside', textinfo='percent')
        
    div = opy.plot(fig, auto_open=False, output_type='div')

    # end of chart
    # *map*
    # csv to check geolocation

    df = pd.read_csv('static/csv/worldcities.csv')
    testing =[]
    test =  Profile.objects.values('Current_Location')
    for i in test:
        testing.append(i['Current_Location'])
    

    count = len(testing)
    # getting geolocation of cities
    lis = []
    lis.append(['city', 'lat', 'lng'])
    for i in testing:
        x = df.loc[df['city'] == i]
        if len(x)==0:
            break
        else:
            l = x.values.tolist()
            
            a = l[0][0]
          
            v = l[0][2]
            u = l[0][3]

        if len(l) > 0:
            lis.append([i, str(v), str(u)])

    with open('static/csv/pro.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(lis)

    us_cities = pd.read_csv("static/csv/pro.csv")
    # figure plotting
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lng", hover_name="city", hover_data=[
                            "city"], color_discrete_sequence=["red"], zoom=3, height=500)

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # show data on template
    div2 = opy.plot(fig, auto_open=False, output_type='div')

    #Bar graph
    df1 = pd.DataFrame(columns=['Branch','Count'])
    val = Profile.objects.values('Branch')
    l=[]
    
    
    # loop for putting all the name into list
    for i in val:
        l.append(i['Branch'])

    
    #to get the distinct value conerted to set
    s=set(l)
    
    comp = len(s)
    for i in s:
        #filtering and fetching the count of same name and putting it in dataframe    
        d=Profile.objects.filter(Branch=i)
        df1=df1.append({'Branch':i,'Count':len(d)},ignore_index=True)

    
    fig3 = px.bar(df1, x='Branch', y='Count',
                hover_data=['Count'], color_discrete_sequence=px.colors.qualitative.Dark24,
                labels={'pop':'Number of Students'}, height=400)
    div3 = opy.plot(fig3, auto_open=False, output_type='div')


    

    d=Profile.objects.all()
    ce=Profile.objects.all()

    # date time
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    today = str(date.today())


    # Progress bar
    paginator = Paginator(d, 5)
    page = request.GET.get('page')
    d = paginator.get_page(page)

    count1 = Blog.objects.filter(status=0).count()

    
    
    D={'d':d,'c':ce,'pie':div,'map':div2,'time':current_time,'date':today,'cities':count,'company':comp,'bar':div3,'name':'Dashboard','count':count1}
    return render(request,'dashboard/home.html',D)


@login_required(login_url='login')
@admin_only
def analytics(request):
    d=Profile.objects.all()
    ce=Profile.objects.all()

    context={'d':d,'c':ce,'name':'Analytics'}
    return render(request,'sidebar_template/analytics.html',context)



@login_required(login_url='login')
@admin_only
def charts(request):
    df = pd.DataFrame(columns=['Name','Count'])

    # fetching all the valuesv of names from the 
    
    val = Profile.objects.values('Company')
    l=[]
    
    
    # loop for putting all the name into list
    for i in val:
        l.append(i['Company'])

    
    #to get the distinct value conerted to set
    s=set(l)
    
    comp = len(s)
    for i in s:
        #filtering and fetching the count of same name and putting it in dataframe    
        d=Profile.objects.filter(Company=i)
        df=df.append({'Name':i,'Count':len(d)},ignore_index=True)
        
        
    

    fig = px.pie(df, values='Count', names='Name',color_discrete_sequence=px.colors.qualitative.Dark24,title='Companies')
    fig.update_traces(textposition='inside', textinfo='percent')
        
    div = opy.plot(fig, auto_open=False, output_type='div')


#Bar graph
    df1 = pd.DataFrame(columns=['Branch','Count'])
    val = Profile.objects.values('Branch')
    l=[]
    
    
    # loop for putting all the name into list
    for i in val:
        l.append(i['Branch'])

    
    #to get the distinct value conerted to set
    s=set(l)
    
    comp = len(s)
    for i in s:
        #filtering and fetching the count of same name and putting it in dataframe    
        d=Profile.objects.filter(Branch=i)
        df1=df1.append({'Branch':i,'Count':len(d)},ignore_index=True)

    
    fig3 = px.bar(df1, x='Branch', y='Count',
                hover_data=['Count'], color_discrete_sequence=px.colors.qualitative.Dark24,
                labels={'pop':'Number of Students'}, height=400)
    div3 = opy.plot(fig3, auto_open=False, output_type='div')



    context={'pie':div,'bar':div3,'name':'Charts'}
    return render(request,'sidebar_template/charts.html',context)


    
@login_required(login_url='login')
@admin_only
def tables(request):
    data=Profile.objects.all()
    
    paginator = Paginator(data, 5)
    page = request.GET.get('page')
    d = paginator.get_page(page)


    context={'d':d,'name':'Tables'}
    return render(request,'sidebar_template/tables.html',context)

@login_required(login_url='login')
@admin_only
def companies(request):
  
    d = Profile.objects.values('Company')

    context={'d':d,'name':'Companies'}
    return render(request,'sidebar_template/company.html',context)


@login_required(login_url='login')
@admin_only
def map(request):
      # *map*
    # csv to check geolocation

    df = pd.read_csv('static/csv/worldcities.csv')
    testing =[]
    test =  Profile.objects.values('Current_Location')
    for i in test:
        testing.append(i['Current_Location'])
    

    count = len(testing)
    # getting geolocation of cities
    lis = []
    lis.append(['city', 'lat', 'lng'])
    for i in testing:
        x = df.loc[df['city'] == i]
        if len(x)==0:
            break
        else:
            l = x.values.tolist()
           
            a = l[0][0]
          
            v = l[0][2]
            u = l[0][3]

        if len(l) > 0:
            lis.append([i, str(v), str(u)])

    with open('static/csv/pro.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(lis)

    us_cities = pd.read_csv("static/csv/pro.csv")
    # figure plotting
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lng", hover_name="city", hover_data=[
                            "city"], color_discrete_sequence=["red"], zoom=3, height=800)

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # show data on template
    div2 = opy.plot(fig, auto_open=False, output_type='div')

 

    context={'map':div2,'name':'Map'}
    return render(request,'sidebar_template/map.html',context)


