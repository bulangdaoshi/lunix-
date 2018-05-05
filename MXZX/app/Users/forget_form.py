from django import forms
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from Users.models import EmailVerifyRecord,UserProfile


class ForgetForm(forms.Form):
    '''
    找回密码验证
    '''
    email = fields.EmailField(
        required=True,
        error_messages={
            'required': '邮箱必填字段',
            'invalid': '邮箱格式不正确',
        }
    )

    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误',
    })

    def clean_email(self):
        '''
        根据邮箱找回密码
        :return:
        '''
        email = self.cleaned_data.get('email',None)
        user = UserProfile.objects.filter(username=email)

        if user:
            return email
        else:
            raise ('用户没有注册或数据库格式化','invalid')

