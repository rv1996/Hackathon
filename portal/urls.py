from django.conf.urls import url
from .views import *
from .ajax import *

urlpatterns = [

    # url(r'^$',home,name="home"),
    url(r'^login/$',login,name="login"),

    #member url
    url(r'^member_login/$',member_login,name="member_login"),
    url(r'^member_dashboard/$',member_dashboard,name="member_dashboard"),
    url(r'^member_question/$',member_question,name="member_question"),
    url(r'^member_history/$',member_history,name="member_history"),
    url(r'^member_history/(?P<pk>\d+)/view/$',member_question_view,name="member_question_view"),

    #department_url
    url(r'^department_login/$', department_login, name="department_login"),
    url(r'^department_dashboard/$',department_dashboard,name="department_dashboard"),
    url(r'^department_view_question/$',department_question,name="department_view_question"),
    url(r'^department_view_question/(?P<pk>\d+)/answer/$',department_question_answer,name="department_answer_question"),
    url(r'^department_view_question/(?P<pk>\d+)/recommend/$',department_recommend,name="department_recommend"),
    url(r'^department_view_question/(?P<pk>\d+)/recommend/recommendation/$',nltk_recommend,name="nltk_recommend"),
    url(r'^department_view_collaborative_question/$',department_view_collaborated_question,name="department_view_collaborative_question"),
    url(r'^department_view_collaborative_question/(?P<pk>\d+)/answer/$',department_view_collaborative_answer,name="department_view_collaborative_answer"),
    url(r'^department_collaboration/$',department_collaboration,name="department_collaboration"),
    url(r'^department_collaboration/(?P<pk>\d+)/answer/$',department_collaboration_answer,name="department_collaboration_answer"),

    #CS urls

    url(r'^cs_dashboard/$', cs_dashboard, name="cs_dashboard"),
    url(r'^cs_dashboard/(?P<pk>\d+)/submit/$', cs_question_update, name="cs_question_updated"),
    url(r'^cs_login/$', cs_login,name="cs_login"),


    url(r'^logout/$', logout, name="logout"),




]

