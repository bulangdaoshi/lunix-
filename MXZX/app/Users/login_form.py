from django import forms
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models import Q,F
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate


from Users.models import UserProfile,EmailVerifyRecord


class LoginForm(forms.Form):
    username = fields.CharField(required=True,max_length=18,
                                error_messages={
                                    'required':'用户名不能为空',
                                    'max_length':'最长不能超过18个字符',
                                    # 'unique':'不能重复，具有唯一性',
                                })

    password = fields.CharField(required=True,max_length=18,min_length=6,

                                validators=[RegexValidator(r'^(?=.*[0-9])(?=.*[a-zA-z])(?=.*[!@#$_\%\^\&\*(\)])[0-9a-zA-Z!@#$_\%\^\&\*(\)]{8,32}$',
                                                           '密码必须包括数字，字母、特殊字符')],
                                error_messages={
                                    'required': '密码不能为空',
                                    'max_length': '最长不能超过18个字符',
                                    'min_length': '最短不能小于6个字符',
                                })

    def clean_username(self):
        """
        最终对所有的字段进行验证
        :return:
        """
        username = self.cleaned_data.get('username',None)
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username)|Q(email=username))
            if user:
                return username
        except UserProfile.DoesNotExist:
            raise ValidationError('用户没有注册','invalid')

        except UserProfile.MultipleObjectsReturned:
            raise ValidationError('用户已注册','invalid')

    def clean_password(self):
        username = self.cleaned_data.get("username",None)
        password = self.cleaned_data.get('password',None)
        #给密码加密
        # password = make_password(password)
        # print(password)
        # user = UserProfile.objects.filter(password=password).count()
        user = authenticate(username=username, password=password)
        if user:
            return password
        else:
            raise ValidationError('用户密码未注册','invalid')

    def clean(self):
        username = self.cleaned_data.get('username',None)
        user = UserProfile.objects.filter(Q(username=username)|Q(mobile=username)|Q(email=username))
        if user[0].is_active:
            pass
        else:
            raise ValidationError('用户未激活，请到邮箱激活账号链接','invalid')
