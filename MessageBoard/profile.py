from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from MessageBoard.forms import AccountCreationForm
from MessageBoard.models import UserProfile
from MessageBoard.tasks import new_user_conf_code_mail, non_activated_user_conf_code_mail

######################################################################################################################


def account_register(request):
    if request.user.is_authenticated:
        return redirect('ads_list')

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = user.username
            user_email = user.email

            if not User.objects.filter(email=user_email).exists():
                user.is_active = False
                user.save()
                new_user_conf_code_mail.delay(user.id)
                messages.info(request, message='Код активации был отправлен Вам по электронной почте.')
                return redirect(to='account_confirm')
            else:
                existing_email_user = User.objects.get(email=user_email)
                if existing_email_user.username != username and existing_email_user.is_active:
                    form = AccountCreationForm()
                    messages.info(request, message='Учетная запись с этим электронным адресом уже существует.')
                    context = {
                        'reg_form': form,
                    }
                    return render(request, template_name='profile/register.html', context=context)
                elif existing_email_user.username != username and not existing_email_user.is_active:
                    existing_email_user.username = username
                    existing_email_user.save()
                    non_activated_user_conf_code_mail.delay(existing_email_user.id)
                    messages.info(
                        request,
                        message='Похоже, Вы уже пытались зарегистрироваться. Новый код активации был отправлен Вам '
                                'по электронной почте'
                    )
                    return redirect(to='account_confirm')
    else:
        form = AccountCreationForm()

    context = {
        'reg_form': form,
    }
    return render(request, template_name='profile/register.html', context=context)


######################################################################################################################


def account_confirm(request):
    if request.user.is_authenticated:
        return redirect('ads_list')
    if request.method == 'POST':
        code = request.POST.get('conf_code')
        if UserProfile.objects.filter(code=code):
            user = UserProfile.objects.get(code=code).user
            user.is_active = True
            user.save()
            UserProfile.objects.get(code=code).delete()
            return redirect(to='login')
        else:
            messages.info(request, message='Неверный код подтверждения.')
    return render(request, template_name='profile/activation.html')


######################################################################################################################


def account_login(request):
    if request.user.is_authenticated:
        return redirect('ads_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect(to='ads_list')
        else:
            messages.info(
                request,
                message='Введено неверное имя пользователя или пароль. Или ваша учетная запись не активирована.'
            )

    context = {}
    return render(request, template_name='profile/login.html', context=context)


######################################################################################################################


def account_logout(request):
    logout(request)
    return redirect(to='login')


######################################################################################################################
