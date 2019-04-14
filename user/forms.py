from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

# 自定义用户登录表单
class LoginForm(forms.Form):
	username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control',
																'placeholder':'请输入用户名'}))
	password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control',
																'placeholder':'请输入密码'}))

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user = auth.authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError('用户名或密码错误！')
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data


# 自定义用户注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(
    	label='用户名',
        max_length=30,
        min_length=3,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'})
    )

    nickname = forms.CharField(
    	label='昵称',
    	max_length=20,
    	required=False,
    	widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入昵称'})
    )
    email = forms.EmailField(
    	label='邮箱',
    	required=False,
     	widget=forms.EmailInput(
        	attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )

    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    password = forms.CharField(
    	label='密码',
    	min_length=6,
        max_length=20,
        widget=forms.PasswordInput(
           	attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )

    password_again = forms.CharField(
    	label='确认密码',
    	min_length=6,
     	max_length=20,
     	widget=forms.PasswordInput(
         	attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次密码不一致')
        return password

    def clean_verification_code(self):
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        
        # 判断验证码是否正确
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code


# 自定义修改昵称表单
class ChangeNicknameForm(forms.Form):
	nickname_new = forms.CharField(
		label='昵称', 
		max_length=20,
		widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}
		)
	)

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(ChangeNicknameForm, self).__init__(*args, **kwargs)

	def clean(self):
		# 判断用户是否登录
		if self.user.is_authenticated:
			self.cleaned_data['user'] = self.user
		else:
			raise forms.ValidationError('用户未登录')
		return self.cleaned_data

	def clean_nickname_new(self):
		nickname_new = self.cleaned_data.get('nickname_new', '').strip()
		if nickname_new == '':
			raise forms.ValidationError("昵称不能为空")
		return nickname_new



# 自定义绑定邮箱表单
class BindEmailForm(forms.Form):
	email = forms.EmailField(
		label='邮箱', 
		widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
		)
	)
	verification_code = forms.CharField(
		label='验证码', 
		required=False,
		widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'点击"发送验证码"发送到邮箱'}
		)
	)

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('该邮箱已经被绑定')
		return email

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code', '').strip()
		if verification_code == '':
			raise forms.ValidationError('验证码不能为空')
		return verification_code

	def __init__(self, *args, **kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(BindEmailForm, self).__init__(*args, **kwargs)

	def clean(self):
		# 判断用户是否登录
		if self.request.user.is_authenticated:
			self.cleaned_data['user'] = self.request.user
		else:
			raise forms.ValidationError('用户未登录')

		# 判断用户是否已经绑定邮箱
		if self.request.user.email != '':
			raise forms.ValidationError('您已经绑定过邮箱')

		# 判断验证码
		code = self.request.session.get('bind_email_code', '')
		verification_code = self.cleaned_data.get('verification_code', '')
		if not (code != '' and code == verification_code):
			raise forms.ValidationError('验证码不正确')

		return self.cleaned_dat

# 自定义修改密码表单
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧密码', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '请输入旧密码'}
        )
    )

    new_password = forms.CharField(
        label='新密码', 
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '请输入新密码'}
        )
    )

    new_password_again = forms.CharField(
        label='确认密码', 
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '请再次输入密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        # 验证旧密码是否正确
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码不正确')
        return old_password

# 自定义找回密码表单
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定的邮箱'}
        )
    )

    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    new_password = forms.CharField(
        label='新密码', 
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '请输入新密码'}
        )
    )

    new_password_again = forms.CharField(
        label='确认密码', 
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '请再次输入密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        
        # 判断验证码是否正确
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code