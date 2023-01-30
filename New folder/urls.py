"""RailwayDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from railway.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',nav,name="nav"),
    path('about/',About,name="about"),
    path('login/',Login_customer,name="login_customer"),
    path('register_customer/',Register_customer,name="register_customer"),
    path('contact/',Contact,name="contact"),
    path('search_train/',Search_Train,name="search_train"),
    path('book_detail/(?P<coun>[0-9]+)/(?P<pid>[0-9]+)/(<str:route1>)',Book_detail,name="book_detail"),
    path('delete_passenger/(?P<pid>[0-9]+)/(?P<bid>[0-9]+)/(<str:route1>)',Delete_passenger,name="delete_passenger"),
    path('dashboard/',Dashboard,name="dashboard"),
    path('card_detail/(?P<total>[0-9]+)/(?P<coun>[0-9]+)/(<str:route1>)/(?P<pid>[0-9]+)',Card_Detail,name="card_detail"),
    path('log_out/',Logout,name="log_out"),
    path('my_booking/',my_booking,name="my_booking"),
    path('delte_my_booking/(?P<pid>[0-9]+)',delte_my_booking,name="delte_my_booking"),
    path('dashboard2/', admindashboard, name="admindashboard"),
    path('addtrain/', Add_train, name="add_train"),
    path('addroute/', add_route, name="add_route"),
    path('edittrain/?P<pid>[0-9]+)', edit, name="edittrain"),
    path('editroute/?P<pid>[0-9]+)', Edit_route, name="editroute"),
    path('delete/?P<pid>[0-9]+)', delete, name="delete"),
    path('delete_route/?P<pid>[0-9]+)', delete_route, name="delete_route"),
    path('viewtrain/', view_train, name="view_train"),
    path('availableroute/', displayroute, name="availableroute"),
    path('viewbookings/', viewbookings, name="viewbookings"),
    path('deletebooking/(?P<pid>[0-9]+)',deletebooking,name="deletebooking"),
    path('view_ticket/(?P<pid>[0-9]+)',view_ticket, name="view_ticket"),
    path('change_image/(?P<pid>[0-9]+)',change_image, name="change_image"),
    path('view_regusers/', view_regusers, name="view_regusers"),
    path('delete_user/<int:pid>',delete_user, name="delete_user"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
