from django import forms
from django.contrib.auth.models import User
from .models import Department


class Member(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        user = None
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(str(e))
        # print(username)

        if user is None:
            raise forms.ValidationError("Username Does' not exist in the database ")
        return username


# Helper Function
def department_choice():

    dept = Department.objects.all()

    DEPARTMENT = ()

    for d in dept:
        data = ((d.department_name, d.department_name),)
        DEPARTMENT = DEPARTMENT + data
    print(DEPARTMENT)
    return DEPARTMENT

class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea,required=True)






class QuestionForm(forms.Form):
    Question = forms.CharField(widget=forms.Textarea)
    type = forms.ChoiceField(choices=(('starred', 'starred'), ('unstarred', 'unstarred')),
                             label="Select the Type of question?", required=True)
    subject = forms.CharField(max_length=500)
    deadline = forms.DateField(widget=forms.SelectDateWidget)

    asking_to = forms.ChoiceField(choices=department_choice(), label="Select Ministry", required=True)

    # widgets = {'deadline': forms.DateInput(format='%d/%m/%Y')}



