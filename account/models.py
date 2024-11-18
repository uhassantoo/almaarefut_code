from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        unique_together = ('email',)
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def send_verification_email(self, subject, message, **kwargs):
        """
        Send an email to this User.
        """
        from_email = 'talhamalik25.tm@gmail.com'
        text_message = strip_tags(message)

        email = EmailMultiAlternatives(
            subject=subject, body=text_message, to=[self.email], from_email=from_email, **kwargs
        )
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)

    def __str__(self):
        return self.email