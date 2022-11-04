from django.shortcuts import render, redirect
from allauth.account import views
from .forms import SignupForm, ProfileForm, UserUpdateForm, ProfileUpdateForm, ProfileFormset
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, resolve_url

User = get_user_model()

#ログイン
class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

#ログアウト
class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/blog/')


#サインアップ(nickname連携)
def newSignupView(request):
    user_form = SignupForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        user.profile.save()
        
        login(request, user)
       
        return redirect('/accounts/login/')

    ctx = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
  
    return render(request, 'blog/signup_form.html', ctx)

#user確認用view
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じか、又はスーパーユーザーなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

#Profile内容確認用view
class ProfileView(OnlyYouMixin, DetailView):
    model = User
    template_name = 'blog/profile.html'

#Profile内容編集用view
class ProfileEditView(OnlyYouMixin, UpdateView):
    model = User
    template_name = 'blog/profile_edit.html'
    form_class = UserUpdateForm
    
    def get_success_url(self): 
            return reverse_lazy("profile", kwargs={"pk": self.request.user.pk}) #入力フォーム内容がセーブできた時の遷移先

    def get_context_data(self, **kwargs):
        
        ctx=super(ProfileEditView, self).get_context_data(**kwargs) #オーバーライド前のget_context_dataで返されるオブジェクトを格納
        
        if self.request.method=="POST": #"POST"が呼び出されたときの処理
            
            ctx.update(dict(user_formset=ProfileFormset(self.request.POST or None,  instance=self.object)))

        else: 
            ctx.update(dict(user_formset=ProfileFormset(self.request.POST or None, instance=self.object)))
            ProfileFormset.extra=0
        
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        user_formset = ctx["user_formset"]

        if user_formset.is_valid():
            self.object=form.save(commit=False)
            self.object.save()  
            user_formset.save()
            return redirect(self.get_success_url())

        else:
            ctx["form"] = form
            return self.render_to_response(ctx)