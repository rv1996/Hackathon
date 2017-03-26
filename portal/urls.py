from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$',home,name="home"),
    url(r'^member_login/$',member_login,name="member_login"),
    url(r'^department_login/$',department_login,name="department_login"),
    url(r'^member_dashboard/$',member_dashboard,name="member_dashboard"),
    url(r'^member_question/$',member_question,name="member_question"),
    url(r'^member_history/$',member_history,name="member_history"),
    url(r'^department_dashboard/$',department_dashboard,name="department_dashboard"),
    url(r'^department_view_question/$',department_question,name="department_view_question"),
    url(r'^department_collaboration/$',department_collaboration,name="department_collaboration"),
    url(r'^logout/$',logout,name="logout"),



]