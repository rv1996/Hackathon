from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$',member_login,name="home"),
    url(r'^member_dashboard/$',member_dashboard,name="member_dashboard"),

]