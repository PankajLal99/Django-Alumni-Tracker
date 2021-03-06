from django.urls import path
from . import views

urlpatterns=[
    path('',views.info,name='info'),
    path('userpage/',views.userpage,name='user'),
    path('profile/<str:pk>/',views.profile,name='profile'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('cruds/<str:pk>/',views.crud,name='cruds'),
    path('delete/<str:pk>/',views.deleteprofile,name='delete'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('post/',views.post,name='post'),
    path('blogs/',views.blog,name='blog'),
    path('allowblog/',views.allowblog,name='requestupdate'),
    path('blogs/<str:pk>/',views.showblog,name='showblog'),
    path("scrapper/",views.scrapper, name="scrapper"),
    path("analytics/",views.analytics, name="analytics"),
    path("charts/",views.charts, name="charts"),
    path("tables/",views.tables, name="tables"),
    path("map/",views.map, name="map"),
    path("companies/",views.companies, name="companies"),
]