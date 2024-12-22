from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User,Profile
from .forms import CustomAdminChangeForm

class UserAdmin(BaseUserAdmin):
    form = CustomAdminChangeForm
    #一覧ページ用
    list_display = (
        "email",
        "active",
        "staff",
        "admin",



    )

    list_filter = (
        "admin",
        "active",
    )
    ordering = ("email",)
    filter_horizontal = ()

    search_fields = ('email',)

    #新規登録用
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')
        }
         
          ),
    )


    #編集ページ用
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('プロフィール',{'fields':(
            'username',
            'affiliation',
            'height',
            'weight',
            'total_score',
            'gender',
            'birthday',
            'gl_point',
        )}),

        ('権限',{'fields':('staff','admin',)}),
    )

admin.site.register(User,UserAdmin)
# admin.site.register(Profile)
