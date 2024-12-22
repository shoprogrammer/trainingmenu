from django import forms
from .models import TrainingModel,SubTrainingModel,MainTrainingModel,Auxiliary
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput


class TrainingForm(forms.ModelForm):
    date = forms.DateField(
        label="作成日",
        widget=DatePickerInput(format='%Y-%m-%d')
    )



    class Meta:
        model = TrainingModel
        fields = ['title','content','date']






class SubTrainingForm(forms.ModelForm):
    
    class Meta:
        model = SubTrainingModel
        fields = ['title','weight','set_number','rep_number','help_training']

class MainTrainingForm(forms.ModelForm):

    class Meta:
        model = MainTrainingModel
        fields = ['title','content','weight','set_number','rep_number','rm']


class AuxiliaryForm(forms.ModelForm):
    class Meta:
        model = Auxiliary
        fields = []