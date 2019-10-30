from django.contrib.auth.models import User
from django import forms
from .models import student,teacher



class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['username','password']
class studentregister(forms.ModelForm):
    class Meta:
        model =student
        fields=['usn','first_name','last_name','email']
class teacherregister(forms.ModelForm):
    class Meta:
        model=teacher
        fields=['pid','first_name','last_name','subcode']

        
class choices_1(forms.Form):
    DISPLAY_CHOICES = (    (1, "Student"),
    (2,"Faculty")
    )
    display_type= forms.ChoiceField(widget=forms.RadioSelect, 
    choices=DISPLAY_CHOICES,label="Please Choose One ")