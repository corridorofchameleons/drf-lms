import os
import secrets

from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, FormView, UpdateView

from users.utils.password_generator import password_generator
from users.forms import UserRegisterForm, PasswordResetForm, UserUpdateForm
from users.models import User
from dotenv import load_dotenv

load_dotenv()


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:email_sent')
    template_name = 'registration/user_form.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/accounts/verification/{token}'
        send_mail(
            subject='Активация аккаунта',
            message=f'Привет, {user.email}!\n\n'
                    f'Для активации перейди по ссылке: {url}\n\n'
                    f'С уважением, команда из одного человека',
            from_email=os.getenv('SMTP_USER'),
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class EmailSentView(TemplateView):
    template_name = 'registration/email_sent.html'


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return render(request, 'registration/user_activated.html')


class PasswordReset(FormView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('users:password_changed')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = get_object_or_404(User, email=email)
        except:
            return redirect(reverse('users:reset_password'))
        else:
            password = password_generator()
            user.password = make_password(password, salt=None, hasher='default')
            user.save()
            send_mail(
                subject='Новый пароль',
                message=f'Привет, {user.email}!\n\n'
                        f'Новый пароль: {password}\n\n'
                        f'С уважением, команда из одного человека',
                from_email=os.getenv('SMTP_USER'),
                recipient_list=[user.email]
            )
            return super().form_valid(form)


class PasswordChanged(TemplateView):
    template_name = 'registration/password_changed.html'


class DataChanged(TemplateView):
    template_name = 'registration/data_changed.html'


class UserUpdate(UpdateView):
    model = User
    template_name = 'registration/update_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:data_changed')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('users:data_changed')
