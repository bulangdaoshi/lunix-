from django import forms
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


from Users.models import EmailVerifyRecord,UserProfile


class RegisterForm(forms.Form):
    email = fields.EmailField(
        required=True,
        error_messages={
            'required':'邮箱必填字段',
            'invalid':'邮箱格式不正确',
        }
    )

    password = fields.CharField(required=True, max_length=18, min_length=6,

                                validators=[RegexValidator(
                                    r'^(?=.*[0-9])(?=.*[a-zA-z])(?=.*[_!@#$\%\^\&\*(\)])[0-9a-zA-Z_!@#$\%\^\&\*(\)]{8,32}$',
                                    '密码必须包括数字，字母、特殊字符')],
                                error_messages={
                                    'required': '密码不能为空',
                                    'max_length': '最长不能超过18个字符',
                                    'min_length': '最短不能小于6个字符',
                                })

    captcha = CaptchaField(error_messages={
        'invalid':'验证码错误',
    })

    def clean_email(self):
        """
        验证邮箱是否已注册
        :return:
        """
        email = self.cleaned_data.get('email',None)
        counts = UserProfile.objects.filter(email=email).count()
        if counts:
            raise ValidationError("用户邮箱已注册",'invalid')
        return email




