from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from Users.login_form import LoginForm
from Users.register_form import RegisterForm
from Users.forget_form import ForgetForm
from Users.reset_pwd import ResetForm
from Users.models import UserProfile,EmailVerifyRecord
from untils.send_email import send_register_email


class Index(View):
    """
    基于类
    """
    def get(self,request):
        return render(request,'index.html')


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)|Q(mobile=username))

            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None
        except UserProfile.MultipleObjectsReturned:
            return None

# def login(request):
#     """
#     django框架自带的登陆效果
#     :param request:
#     :return:
#     """
#     if request.method =="GET":
#         return render(request,'login.html')
#     elif request.method == "POST":
#         current_account = request.POST.get('account',None)
#         current_password = request.POST.get('password',None)
#         user = authenticate(username=current_account,password=current_password)
#         if user is not None:
#             login(request,user)
#             return redirect('http://127.0.0.0.1:8000/')
#         else:
#             return render(request,'login.html')


#详细的功能我就没有写了
def login(request):
    """
    用户登录效果,要熟练的掌握session和cookies
    :param request:
    :return:
    """
    if request.method == "GET":
        login_forms = LoginForm()
        return render(request,'login.html',{'login_forms':login_forms})

    elif request.method == "POST":
        login_forms = LoginForm(request.POST)
        print('yonghuming',login_forms.errors)
        if login_forms.is_valid():
            username=login_forms.cleaned_data['username']
            request.session['user'] = username

            # print(request.session['user'])
            # print('Cookies',request.COOKIES)
            return redirect("/user/index/")

        return render(request,'login.html',{'login_forms':login_forms})


class Register(View):
    """
    用户注册
    """

    def get(self,request):
        """
        get方法获取
        :param request:
        :return:
        """
        register_form = RegisterForm()
        return render(request,'register.html',{"register_form":register_form})

    def post(self,request):

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            password_encrypt = make_password(password)
            UserProfile.objects.create(
                email=email,
                password = password_encrypt,
                username = email,
                is_active = False,
            )

            #这里要判断用户是否激活我就没有判断了
            # user = UserProfile()
            # user.is_active=True
            send_register_email(email=email, send_type='register')

            return HttpResponse("暂时页面就是这样，请点开邮箱激活账户开通GPS导航，"
                                "跳转登录页面，我还回来的！！！")

        return render(request,'register.html',{'register_form':register_form})


class ActiveUser(View):
    """
    激活用户的邮箱密码
    """
    def get(self, request, active_code):

        active_user = EmailVerifyRecord.objects.filter(code=active_code)

        if active_user:
            for active in active_user:
                email = active.email

                #更为简便的方法
                #UserProfile.objects.filter(email=email).updata(is_active=True)

                user = [user for user in UserProfile.objects.filter(email=email)]
                user[0].is_active = True
                user[0].save()
                request.session['email']=email
            return render(request,'active_user.html')

        return render(request,'active_fail.html')


class ForgetPwd(View):
    """
    用户找回密码功能；
    """
    def get(self,request):
        forger_forms = ForgetForm()
        return render(request,'forgetpwd.html',{"forger_forms":forger_forms})

    def post(self,request):
        forger_forms = ForgetForm(request.POST)
        if forger_forms.is_valid():
            email = forger_forms.cleaned_data.get('email',None)
            send_register_email(email=email, send_type='forget')

            return HttpResponse("找回密码链接已发送到你的邮箱，请查收，点击激活找回密码")

        return render(request,'forgetpwd.html',{'forger_forms': forger_forms})


class ResetUserPwd(View):
    """
    显示密码找回是否召回
    """
    def get(self,request,active_code):
        reset_pwds = EmailVerifyRecord.objects.filter(code=active_code)
        if reset_pwds:
            email = reset_pwds[0].email
            request.session['email'] = email
            return render(request,'reset_success.html')
        return render(request,'reset_fail.html')


class ModifyUserPwd(View):
    """
     激活链接后，找回密码，重置密码
    """
    def get(self,request):
        email = request.session['email']
        return render(request,'password_reset.html',{'email': email})

    def post(self,request):
        reset_form = ResetForm(request.POST)
        email = request.POST.get('email',None)
        if reset_form.is_valid():
            pwd = reset_form.cleaned_data['password1']
            UserProfile.objects.filter(Q(username=email)|Q(email=email)).update(password=make_password(pwd))
            return redirect("/user/login/")

        return render(request,'password_reset.html',{'reset_form': reset_form})


def logout_view(request):
    logout(request)
    return redirect("/user/index/")