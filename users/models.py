from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

import uuid 


#ここ( https://github.com/django/django/blob/master/django/contrib/auth/models.py#L321 )から流用
class CustomUser(AbstractBaseUser, PermissionsMixin):

    username_validator  = UnicodeUsernameValidator()

    id          = models.UUIDField( default=uuid.uuid4, primary_key=True, editable=False )
    username    = models.CharField(
                    _('username'),
                    max_length=150,
                    unique=True,
                    help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                    validators=[username_validator],
                    error_messages={
                        'unique': _("A user with that username already exists."),
                    },
                )

    first_name  = models.CharField(_('first name'), max_length=150, blank=True)
    last_name   = models.CharField(_('last name'), max_length=150, blank=True)

    #メールの入力を必須化。
    email       = models.EmailField(_('email address'))

    is_staff    = models.BooleanField(
                    _('staff status'),
                    default=False,
                    help_text=_('Designates whether the user can log into this admin site.'),
                )

    is_active   = models.BooleanField(
                    _('active'),
                    default=True,
                    help_text=_(
                        'Designates whether this user should be treated as active. '
                        'Unselect this instead of deleting accounts.'
                    ),
                )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects     = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    #createsuperuserを実行し、メールアドレスを入力必須化させる。
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True #この指定がないとカスタムユーザーモデルは反映されず、マイグレーションエラーになる。

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
