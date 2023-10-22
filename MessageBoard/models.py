from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

######################################################################################################################


CATEGORIES = [
    ('Tank', 'Танк'),
    ('Healer', 'Хил'),
    ('DamageDealer', 'ДД'),
    ('Trader', 'Торговец'),
    ('GuildMaster', 'Гилдмастер'),
    ('QuestGiver', 'Квестгивер'),
    ('Warsmith', 'Кузнец'),
    ('Tanner', 'Кожевник'),
    ('PotionMaker', 'Зельевар'),
    ('SpellMaster', 'Мастера заклинаний'),
]


######################################################################################################################


class UserProfile(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    activation_code = models.CharField(
        max_length=9,
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user.get_full_name()}'

    class Meta:
        ordering = 'user',
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        managed = True


######################################################################################################################


class Advertisement(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор объявления',
        related_name='Author_Advertisement',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Заголовок объявления',
        max_length=255,
        default='',
    )
    content = RichTextUploadingField(
        verbose_name='Текст объявления',
        blank=True,
    )
    category = models.CharField(
        verbose_name='Категория',
        choices=CATEGORIES,
        max_length=12,
        default=None,
        null=True,
        blank=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания объявления',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = 'title',
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        managed = True


######################################################################################################################


class Comment(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отклика',
        related_name='Author_Comment',
        on_delete=models.CASCADE,
    )
    advertisement = models.ForeignKey(
        Advertisement,
        verbose_name='Объявление',
        related_name='Advertisement_Comment',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст отклика',
        blank=True,
        default='',
    )
    is_approved = models.BooleanField(
        verbose_name='Одобрено',
        default=False,
    )
    is_rejected = models.BooleanField(
        verbose_name='Отклонен',
        default=False,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания отклика',
        auto_now_add=True,
        null=True,
    )

    def approve(self):
        self.is_approved = True
        self.save()

    def disapprove(self):
        self.is_approved = False
        self.save()

    def reject(self):
        self.is_rejected = True
        self.save()

    def accept(self):
        self.is_rejected = False
        self.save()

    def __str__(self):
        return f'{self.text[:30]}...'

    class Meta:
        ordering = 'text',
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        managed = True


######################################################################################################################
