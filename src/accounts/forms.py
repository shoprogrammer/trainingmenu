from django import forms
from django.forms.fields import DateField
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm

from .models import User,Profile,GENDER_CHOICE

class CustomAdminChangeForm(UserChangeForm):
    #profileクラスのフィールドを追記します
    username = forms.CharField(max_length=100)
    affiliation = forms.CharField(max_length=100)
    height = forms.IntegerField()
    weight = forms.IntegerField()
    total_score = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birthday = DateField()
    gl_point = forms.FloatField()

    class Meta:
        model = User
        fields = ('email','password','active','admin')
    
    #profileが存在する場合は、初期値にデータを格納する
    def __init__(self,*args,**kwargs):
        user_obj = kwargs["instance"]
        if hasattr(user_obj,"profile"):
            profile_obj = user_obj.profile
            self.base_fields["username"].initial = profile_obj.username
            self.base_fields["affiliation"].initial = profile_obj.affiliation
            self.base_fields["height"].initial = profile_obj.height
            self.base_fields["weight"].initial = profile_obj.weight
            self.base_fields["total_score"].initial = profile_obj.total_score
            self.base_fields["gender"].initial = profile_obj.gender
            self.base_fields["birthday"].initial = profile_obj.birthday
            self.base_fields['gl_point'].initial = profile_obj.gl_point
        super().__init__(*args,**kwargs)


    #保存機能の定義
    def save(self,commit=True):
        user_obj = super().save(commit=False)
        username = self.cleaned_data.get("username")
        affiliation = self.cleaned_data.get("affiliation")
        height = self.cleaned_data.get("height")
        weight = self.cleaned_data.get("weight")
        total_score = self.cleaned_data.get("total_score")
        gender = self.cleaned_data.get("gender")
        birthday = self.cleaned_data.get("birthday")
        gl_point = self.cleaned_data.get('gl_point')
        if hasattr(user_obj,"profile"):
            profile_obj = user_obj.profile
        else:
            profile_obj = Profile(user=user_obj)
        if username is not None:
            profile_obj.username = username
        if affiliation is not None:
            profile_obj.affiliation = affiliation
        if height is not None:
            profile_obj.height = height
        if weight is not None:
            profile_obj.weight = weight
        if total_score is not None:
            profile_obj.total_score = total_score
        if gender is not None:
            profile_obj.gender = gender
        if birthday is not None:
            profile_obj.birthday = birthday
        if gl_point is not None:
            profile_obj.gl_point = gl_point
        profile_obj.save()
        if commit:
            user_obj.save()
        return user_obj
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_email = self.instance.user.email
        if username == user_email:
            raise forms.ValidationError("ユーザー名を変更してください")
        elif "@" in username:
            raise forms.ValidationError("ユーザー名にEメールアドレスは使用できません")
        return username