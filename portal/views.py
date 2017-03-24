from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import Member,Question
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.



def member_login(request):


    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("member_dashboard"))



    form = Member(request.POST or None)

    if request.method=="POST":
        form = Member(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect(reverse("member_dashboard"))

    context = {
        "title":"Login page",
        "form":form,
    }
    return render(request,"portal/home.html",context=context)


def member_dashboard(request):


    try:
        user = User.objects.get(username=request.user)
        print(user.department)
        return HttpResponseRedirect(reverse('department_dashboard')) #user might not not be a department
    except Exception as e:
        pass

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("member_login"))



    form = Question(request.POST or None)
    context = {
        "title":"Welcome to Dashboard page",
        "form":form,
    }
    if request.method == "POST":
        form = Question(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data )


    return render(request,"portal/member_dashboard.html",context)


def department_dashboard(request):
    context = {
        "title":"Welcome to Department DashBoard",
    }
    return render(request,"portal/department_dashboard.html",context)