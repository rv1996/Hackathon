import json
from django.http import HttpResponse
from .models import Question, QuestionFor


def nltk_recommend(request,pk):

    question = Question.objects.get(pk=pk)
    question_text = question.text

    query_set = {
        "name":"rupanshu",
    }

    return HttpResponse(json.dumps(query_set), content_type="application/json")