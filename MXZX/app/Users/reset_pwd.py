from django import forms
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class ResetForm(forms.Form):
    '''
    重置密码和密码验证
    '''
    password1 = fields.CharField(required=True, max_length=18, min_length=6,

                                validators=[RegexValidator(
                                    r'^(?=.*[0-9])(?=.*[a-zA-z])(?=.*[_!@#$\%\^\&\*(\)])[0-9a-zA-Z_!@#$\%\^\&\*(\)]{8,32}$',
                                    '密码必须包括数字，字母、特殊字符')],
                                error_messages={
                                    'required': '密码不能为空',
                                    'max_length': '最长不能超过18个字符',
                                    'min_length': '最短不能小于6个字符',
                                })

    password2 = fields.CharField(required=True, max_length=18, min_length=6,

                                validators=[RegexValidator(
                                    r'^(?=.*[0-9])(?=.*[a-zA-z])(?=.*[_!@#$\%\^\&\*(\)])[0-9a-zA-Z_!@#$\%\^\&\*(\)]{8,32}$',
                                    '密码必须包括数字，字母、特殊字符')],
                                error_messages={
                                    'required': '密码不能为空',
                                    'max_length': '最长不能超过18个字符',
                                    'min_length': '最短不能小于6个字符',
                                })

    def clean(self):
        pwd1 = self.cleaned_data.get('password1',None)
        pwd2 = self.cleaned_data.get('password2',None)
        if pwd1 == pwd2:
            pass
        else:
            raise ValidationError("密码不一致",'invalid')
