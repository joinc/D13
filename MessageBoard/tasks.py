from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from MessageBoard.passwords import one_time_password
from MessageBoard.models import UserProfile, User, Comment

######################################################################################################################


@shared_task
def new_user_conf_code_mail(user_id):
    activation_code = one_time_password()
    new_user = User.objects.get(id=user_id)
    new_user_code = UserProfile.objects.create(user=new_user, activation_code=conf_code)
    new_user_name = new_user_code.user.username
    new_user_email = new_user_code.user.email
    mail_subj = 'Подтверждение учетной записи'
    message = render_to_string(
        template_name='email/account_activate.html',
        context={
            'username': new_user_name,
            'activation_code': activation_code,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[new_user_email],
    )
    email.send()


######################################################################################################################


@shared_task
def non_activated_user_conf_code_mail(user_id):
    new_activation_code = one_time_password()
    non_activated_user = User.objects.get(id=user_id)
    old_conf_code = UserProfile.objects.get(user=non_activated_user)
    old_conf_code.activation_code = new_activation_code
    old_conf_code.save()
    non_activated_username = non_activated_user.username
    non_activated_email = non_activated_user.email

    mail_subj = 'Новый код подтверждения'
    message = render_to_string(
        template_name='email/account_activate.html',
        context={
            'username': non_activated_username,
            'activation_code': new_activation_code,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[non_activated_email],
    )
    email.send()


######################################################################################################################


@shared_task
def weekly_non_active_users_and_codes_clear():
    non_active_users = User.objects.filter(is_active=False)
    for user in non_active_users:
        user.delete()

    unused_codes = UserProfile.objects.all()
    for activation_code in unused_codes:
        activation_code.delete()


######################################################################################################################


@shared_task
def new_reply_notify(reply_id):
    repl = Comment.objects.get(id=reply_id)
    ad = repl.adv
    ad_author = ad.author.username
    ad_title = ad.title
    repl_text = repl.text
    repl_author = repl.author.username
    ad_author_email = ad.author.email

    mail_subj = 'Новый отклик на Ваше объявление!'
    message = render_to_string(
        template_name='email/new_comment.html',
        context={
            'ad_author': ad_author,
            'ad_title': ad_title[:25] + '...',
            'reply_text': repl_text[:50] + '...',
            'reply_author': repl_author,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[ad_author_email],
    )
    email.send()


######################################################################################################################


@shared_task
def reply_status_notify(reply_id, status):
    repl = Comment.objects.get(id=reply_id)
    repl_author_name = repl.author.username
    repl_text = repl.text
    ad = repl.adv
    ad_title = ad.title
    ad_author = ad.author.username
    repl_author_email = repl.author.email

    mail_subj = 'Статус Вашего отклика изменился.'
    message = render_to_string(
        template_name='email/comment_status_changed.html',
        context={
            'ad_author': ad_author,
            'ad_title': ad_title[:25] + '...',
            'reply_text': repl_text[:50] + '...',
            'reply_author': repl_author_name,
            'status': status,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[repl_author_email],
    )
    email.send()


######################################################################################################################
