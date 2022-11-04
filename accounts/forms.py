from django import forms
from blog.models import * 
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'nickname'}


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#https://daeudaeu.com/django-user-onetoonefield/


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    """ユーザー情報(nickname)更新フォーム"""
    class Meta:
        model = Profile
        fields = ('nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

#プロフィール　インラインフォームセット
ProfileFormset = forms.inlineformset_factory(
    User, Profile, fields='__all__',
    form=ProfileUpdateForm,  #追加したフォームを渡す
    extra=1,  can_delete=False
)

