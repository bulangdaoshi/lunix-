import re

from django import forms
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from Openation.models import UserAsk


class AskForm(forms.ModelForm):
    '''
    ModelForm,其实我很少用这个
    因为这个很容易出问题
    '''
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile',None)
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise ValidationError("手机号码非法","invalid")

