from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import Member, QuestionForm, AnswerForm
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Question, Department, QuestionFor
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    context = {
        "title": "welcome to home page",
    }
    return render(request, "portal/home.html", context)


def department_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("member_dashboard"))

    form = Member(request.POST or None)
    context = {
        "title": "Login page",
        "form": form,
    }
    if request.method == "POST":
        form = Member(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            dept_user = User.objects.get(username=username)
            try:
                print(dept_user.department)
            except Exception as e:
                messages.warning(request, "Not the official member of ministry")
                return render(request, "portal/department_login.html", context=context)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("department_dashboard"))

    return render(request, "portal/department_login.html", context=context)


def member_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("member_dashboard"))

    form = Member(request.POST or None)
    context = {
        "title": "Login page",
        "form": form,
    }
    if request.method == "POST":
        form = Member(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # here we have to check that the member should be an MP and not the department member.
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("member_dashboard"))

    return render(request, "portal/mp_login.html", context=context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


def member_dashboard(request):
    context = {
        "title": "You can chose your options",
    }

    return render(request, "portal/member_dashboard.html", context)


def member_question(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("member_login"))

    form = QuestionForm(request.POST or None)
    context = {
        "title": "Welcome to Dashboard page",
        "form": form,
    }
    if request.method == "POST":
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            question = form.cleaned_data['Question']
            type = form.cleaned_data['type']
            asking_to = form.cleaned_data['asking_to']
            subject = form.cleaned_data['subject']
            deadline = form.cleaned_data['deadline']
            department = Department.objects.get(department_name=asking_to)
            user = User.objects.get(username=request.user)
            question = Question.objects.create(text=question, type=type, asked_by=user, deadline=deadline,
                                               subject=subject)
            questionfor = question.questionfor_set.create(asked_to=department)
            messages.success(request, "Thank you for your time, The department will reply as soon as possible")
            return redirect(reverse('member_dashboard'))

    return render(request, "portal/member_question.html", context)


def member_history(request):
    question = Question.objects.all().filter(asked_by=User.objects.get(username=request.user)).order_by('-timestamp')

    question = QuestionFor.objects.all().filter()


    context = {
        'title': "Question asked by you",
        'question': question
    }
    return render(request, "portal/member_question_history.html", context)



def member_question_view(request,pk):

    question = Question.objects.get(pk=pk)

    answered_question = question.questionfor_set.all().filter(answer__isnull=False)
    print(answered_question)

    context = {
        'title':"View the answer response",
        "answered_question":answered_question
    }

    return render(request,"portal/member_view_question.html",context)


def department_dashboard(request):
    context = {
        'title': "Welcome to the dash board",
    }
    return render(request, "portal/department_dashboard.html", context)


def department_question_answer(request, pk):
    question = Question.objects.get(pk=pk)
    form = AnswerForm(request.POST or None)

    print(question.type)

    if request.method == "POST":
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            form_answer = form.cleaned_data['answer']
            department = Department.objects.get(user=User.objects.get(username=request.user))
            answer = QuestionFor.objects.get(question=question, asked_to=department)
            answer.answer = form_answer
            answer.save()

            messages.success(request, "Thank you for your time, Mp will get the update regarding this question")
            return HttpResponseRedirect(reverse('department_dashboard'))

    context = {
        'title': "Give your answer here",
        'form': form,
        'question': question,

    }

    return render(request, "portal/department_question_answer.html", context)


def department_recommend(request, pk):

    question = Question.objects.get(pk=pk)

    departments = Department.objects.all().exclude(user=User.objects.get(username=request.user))
    # update the filter query so that one department can only be recommended once only

    print(request.POST.getlist('recommend'))
    context = {
        "title":"Select which department you wanna recommend",
        "recommend":departments,
        "question":question,
    }
    return render(request,"portal/department_question_recommend.html", context)



def department_collaboration(request):
    context = {
        'title': "Collaboraion Help"
    }
    return render(request, "portal/department_view_collaboration.html", context)


def department_question(request):
    dept_user = Department.objects.get(user=User.objects.get(username=request.user))

    question = QuestionFor.objects.all().filter(asked_to=dept_user,answer=None)

    context = {
        "title": "Welcome to Department DashBoard",
        'question': question
    }
    return render(request, "portal/department_view_question.html", context)
