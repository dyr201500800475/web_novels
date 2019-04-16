import string
import random
import time

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile

# 进入登录页面
def login(request):
	redirect_to = request.GET.get('from', '/')
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request, user)
			return redirect(redirect_to)
	else:
		login_form = LoginForm()
	context = {}
	context['login_form'] = login_form
	return render(request, 'user/login.html', context)

# 浮窗登录
def login_for_modal(request):
	data = {}
	login_form = LoginForm(request.POST)
	if login_form.is_valid():
		user = login_form.cleaned_data['user']
		auth.login(request, user)
		data['status'] = 'SUCCESS'
	else:
		data['status'] = 'ERROR'
	return JsonResponse(data)

# 用户退出登录
def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from', '/'))

# 进入注册页面
def register(request):
    redirect_to = request.GET.get('from', '/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            nickname = register_form.cleaned_data['nickname']
            email = register_form.cleaned_data['email']
            # 注册成功创建新用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 保存用户的昵称
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = nickname
            profile.save()
            # 清除session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(redirect_to)
    else:
        register_form = RegisterForm()

    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)

# 进入用户个人中心
def user_info(request):
	context = {}
	return render(request, 'user/base_info.html', context)

# 修改昵称模块
def change_nickname(request):
	redirect_to = request.GET.get('from', '/')
	if request.method == "POST":
		form = ChangeNicknameForm(request.POST, user=request.user)
		if form.is_valid():
			nickname_new = form.cleaned_data['nickname_new']
			profile, created = Profile.objects.get_or_create(user=request.user)
			profile.nickname = nickname_new
			profile.save()
			return redirect(redirect_to)
	else:
		form = ChangeNicknameForm()

	context = {}
	context['page_title'] = '修改昵称'
	context['form_title'] = '修改昵称'
	context['submit_text'] = '修改'
	context['form'] = form
	context['return_back_url'] = redirect_to
	return render(request, 'form.html', context)

# 绑定邮箱模块
def bind_email(request):
	redirect_to = request.GET.get('from', '/')
	if request.method == "POST":
		form = BindEmailForm(request.POST, request=request)
		if form.is_valid():
			email = form.cleaned_data['email']
			request.user.email = email
			request.user.save()
			# 清除session
			del request.session['bind_email_code']
			return redirect(redirect_to)
	else:
		form = BindEmailForm()

	context = {}
	context['page_title'] = '绑定邮箱'
	context['form_title'] = '绑定邮箱'
	context['submit_text'] = '绑定'
	context['form'] = form
	context['return_back_url'] = redirect_to
	return render(request, 'user/bind_email.html', context)

# 发送验证码模块
def send_verfication_code(request):
	email = request.GET.get('email', '')
	send_for = request.GET.get('send_for', '')
	print(email)
	data = {}
	if email != '':
		# 生成验证码
		code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
		now = int(time.time())
		send_code_time = request.session.get('send_code_time', 0)
		if now - send_code_time < 30:
			data['status'] = 'ERROR'
		else:
			request.session[send_for] = code
			request.session['send_code_time'] = now
			# 发送邮件
			send_mail(
				'绑定邮箱',
			    '验证码： %s' % code,
			    '870850834@qq.com',
			    [email],
			    fail_silently=False,
			)
			data['status'] = 'SUCCESS'
	else:
		data['status'] = 'ERROR'
	return JsonResponse(data)

# 修改密码模块
def change_password(request):
    redirect_to = request.GET.get('from', '/')
    print(redirect_to)
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect('user:login')
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


# 忘记密码模块
def forgot_password(request):
    redirect_to = request.GET.get('from', '/')
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '忘记密码'
    context['form_title'] = '忘记密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)