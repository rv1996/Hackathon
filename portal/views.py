from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect,HttpResponse
from .forms import Member, QuestionForm, AnswerForm , Cs_admissable
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Question, Department, QuestionFor, Recommendation
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings



# Create your views here.


def login(request):
    form = Member(request.POST or None)

    context = {
        "title": "welcome to home page",
        "form":form,
    }
    return render(request, "portal/login.html", context)


def cs_login(request):
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
            # dept_user = User.objects.get(username=username)

            user = auth.authenticate(username=username, password=password)

            official_user = User.objects.get(username=username)
            if not official_user.is_superuser:
                messages.success(request,"Not an official member")
                return HttpResponseRedirect(reverse("login"))

            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("cs_dashboard"))

    return render(request, "portal/cs_dashboard.html", context=context)



def department_login(request):
    # if request.user.is_authenticated() and not request.session.get('is_member'):
    #     return HttpResponseRedirect(reverse("member_dashboard"))

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
                return HttpResponseRedirect(reverse('login'))
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("department_dashboard"))

    return render(request, "portal/department_login.html", context=context)


def member_login(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse("member_dashboard"))

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

            # dept = {}



            try:
                dept = Department.objects.get(user=User.objects.get(username=username))
                messages.success(request, "Please enter your valid credentials")
                return HttpResponseRedirect(reverse('login'))
            except Exception as e:
                pass
            #
            #
            #
            # if dept.department_name != '':
            #     messages.success(request,"Please enter your valid credentials")
            #     return HttpResponseRedirect(reverse('login'))


            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session['is_member'] = True
                return HttpResponseRedirect(reverse("member_dashboard"))

    return render(request, "portal/mp_login.html", context=context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


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
            question.save()
            questionfor.save()
            messages.success(request, "Thank you for your time, The department will reply as soon as possible")
            return redirect(reverse('member_dashboard'))

    return render(request, "portal/member_question.html", context)


def member_history(request):
    question = Question.objects.all().filter(asked_by=User.objects.get(username=request.user)).order_by('-timestamp')

    context = {
        'title': "Question asked by you",
        'question': question,
    }
    return render(request, "portal/member_question_history.html", context)



def member_question_view(request,pk):

    question = Question.objects.get(pk=pk)

    answer = QuestionFor.objects.get(question=question)

    print(answer.answer)
    print(answer.asked_to.department_name)


    # print(answered_question)


    context = {
        'title':"View the answer response",
        # "answered_question":answered_question,
        # "not_answered":not_answer,
        'answer':answer,
        "question":question,

    }

    return render(request,"portal/member_view_question.html",context)


def department_dashboard(request):
    context = {
        'title': "Welcome to the dash board",
    }
    return render(request, "portal/department_dashboard.html", context)


def department_question_answer(request, pk):
    question = QuestionFor.objects.get(question = Question.objects.get(pk=pk))
    form = AnswerForm(request.POST or None)

    current_dept = Department.objects.get(user=User.objects.get(username=request.user))

    recommeded_response = current_dept.recommended_by_me.all()

    for q in recommeded_response:
        print(q.question)
        print(q.to.department_name) # ---> recommended to the ministry
        print(q.by.department_name) # ---> current department




    # print(question.type)

    if request.method == "POST":
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            form_answer = form.cleaned_data['answer']
            department = Department.objects.get(user=User.objects.get(username=request.user))
            answer = QuestionFor.objects.get(question=question.question, asked_to=department)
            answer.answer = form_answer
            answer.save()

            messages.success(request, "Thank you for your time, Mp will get the update regarding this question")
            return HttpResponseRedirect(reverse('department_dashboard'))

    answered = False
    if question.answer is not None:
        answered = True
    print('--------')
    print(question.answer)


    context = {
        'title': "Give your answer here",
        'form': form,
        'question': question.question,
        'answered':answered,
        'answer':question.answer,
        'recommeded_response':recommeded_response,

    }

    if question.question.type == 'starred':
        context['starred'] = True
        return render(request, "portal/department_answer_oral.html", context)
    else:
        return render(request, "portal/department_question_answer.html", context)



def department_recommend(request, pk):

    question = Question.objects.get(pk=pk)


    departments = Department.objects.all().exclude(user=User.objects.get(username=request.user))

    current_department = Department.objects.get(user=User.objects.get(username=request.user))

    recommend_list = request.POST.getlist('select')
    print(recommend_list)
    dept = User.objects.get(username=request.user)

    if request.method == "POST":
        for d in recommend_list:
            current_department.recommended_by_me.create(to=Department.objects.get(user=User.objects.get(username=d)),question=question)
            messages.success(request,"Recommendation request has been send you'll be notified  as the ministry reply the answer")
            question.is_recommeded = True
            question.save()
            return HttpResponseRedirect(reverse('department_dashboard'))
    # recommend_object_list = []






    context = {
        "title":"Select which department you wanna recommend",
        "recommend":departments,
        "question":question,
    }
    return render(request,"portal/department_question_recommend.html", context)



def department_collaboration(request):

    current_dept = Department.objects.get(user=User.objects.get(username=request.user))
    recommendation = current_dept.recommended_to_me.all()

    context = {
        'title': "Collaborative Help",
        'recommendation':recommendation,
    }
    return render(request, "portal/department_collaboration_view.html", context)




def department_collaboration_answer(request,pk):
    question = Question.objects.get(pk=pk)

    current_dept = Department.objects.get(user=User.objects.get(username=request.user))
    form = AnswerForm(request.POST or None)
    context = {
        'title':"Department collaborative reply",
        'form':form,
        'question':question,

    }

    if request.method == "POST":
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            q = question.recommendation_set.get(to=current_dept)
            q.recommended_answer = answer
            q.save()
            messages.success(request,"Recommended quesiton is addressed ")
            return HttpResponseRedirect(reverse('department_dashboard'))

    return render(request,"portal/department_collaboration_answer.html",context)


def department_view_collaborated_question(request):
    dept = Department.objects.get(user=User.objects.get(username=request.user))
    recommend_question = dept.recommended_by_me.all()

    print(recommend_question)

    context = {
        "title":"Question that you have asked to other ministry",
        "recommend_question":recommend_question,
    }

    return render(request,"portal/department_view_collaborated_question.html",context)

def department_view_collaborative_answer(request,pk):
    dept = Department.objects.get(user=User.objects.get(username=request.user))
    question = Question.objects.get(pk=pk)
    recommend_question = question.recommendation_set.all()

    print(recommend_question)

    context = {
        "title":"Answe by ministry",
        "recommend_question": recommend_question,
        "question":question,

    }

    return render(request,"portal/department_view_collaborative_answer.html",context)

def department_question(request):
    dept_user = Department.objects.get(user=User.objects.get(username=request.user))

    #possible to query via foreign key reference

    question = QuestionFor.objects.all().filter(asked_to=dept_user,question__is_admisable=True)
    print(question)



    context = {
        "title": "Welcome to Department DashBoard",
        'questions': question,
    }
    return render(request, "portal/department_view_question.html", context)


def cs_dashboard(request):
    form = Cs_admissable(request.POST or None)
    question_list = QuestionFor.objects.all().filter(question__is_admisable=False,question__is_admissed=False)

    paginator = Paginator(question_list, 2)

    page = request.GET.get('page')
    try:
        question = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question = paginator.page(paginator.num_pages)
    #
    # print(question.has_previous(),question.next_page_number(),question.number,question.has_next())

    context = {
        'title': "Central authority to qualify questions",
        'form': form,
        'question': question,
    }

    return render(request, 'portal/cs_dashboard.html', context)


def cs_question_update(request,pk):

    question = Question.objects.get(pk=pk)
    question.type = request.POST.get('type')

    if request.POST.get('admissable') == 'True':
        question.is_admisable = True
    else:
        question.is_admisable = False

    question.is_admissed = True

    data = QuestionFor.objects.get(question=question)
    if question.is_admisable :
        data = QuestionFor.objects.get(question=question)
        email =[str(data.asked_to.user.email)]
        context = {
            'title':'You have a new quesiton to be answered',
            'send_by':data.question.asked_by.username,
            'send_to':data.asked_to.department_name,
            'subject':data.question.subject,
            'type':data.question.type,
            'question':data.question.text,
        }
        send_email(email=email,content=context)
        email_new = [str(data.question.asked_by.email)]
        context_new = {
            'title': 'Your question is addressed by the GS',
            'send_by': data.question.asked_by.username,
            'send_to': data.asked_to.department_name,
            'subject': data.question.subject,
            'type': data.question.type,
            'question': data.question.text,
        }
        send_email(email=email_new, content=context_new)

    else:
        email = [str(data.question.asked_by.email)]
        context = {
            'title': 'Your quesiton is not admissable in the parliament ',
            'send_by': data.asked_to.department_name,
            'send_to': data.question.asked_by,
            'subject': data.question.subject,
            'type': data.question.type,
            'question': data.question.text,
        }
        send_email(email=email, content=context)


    question.save()

    messages.success(request, "Thank you for your time , The question is send to the respective ministry!")

    return HttpResponseRedirect(reverse('cs_dashboard'))


def send_email(email,content=None):
    html_content=render_to_string('portal/emailtemplate.html',{'content':content})
    print(content)
    text_content=strip_tags(html_content)
    print(text_content)
    subject="reminder"
    email_to=email
    email_from=settings.EMAIL_HOST_USER
    msg=EmailMultiAlternatives(subject,text_content,email_from,email_to)
    msg.send()

