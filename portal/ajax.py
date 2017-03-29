import json
from django.http import HttpResponse
from .models import Question, QuestionFor
from nltk_analyse import analyse as nltk

def nltk_recommend(request,pk):

    question = Question.objects.get(pk=pk)
    question_text = question.text
    ministry = nltk.analyse_keywords(question_text)
    names = []
    for m in ministry:
        data = m.split('/')
        names.append(data[-1])

    print(names)

    query_set = {
        "name":"rupanshu",
        "recommend":names[0:2],
    }

    return HttpResponse(json.dumps(query_set), content_type="application/json")