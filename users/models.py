from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self, email, name=None, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			name=name
		)

		user.set_password(password)
		user.is_active = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, name=None):
		user = self.create_user(email, name, password=password)
		user.is_admin = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)
		return user

	def active(self):
		return self.model.objects.filter(is_active=True)


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=100, unique=True)
	name = models.CharField(max_length=255, null=True, default='')
	is_active = models.BooleanField(default=False)
	objects = UserManager()
	wepayUserId = models.CharField(max_length=100, null=True, default='')
	wepayAccountId = models.CharField(max_length=100, null=True, default='')
	wepayAccessToken = models.CharField(max_length=100, null=True, default='')


	USERNAME_FIELD = 'email'

	def get_full_name(self):
		return self.name if self.name else self.email

	def get_short_name(self):
		return self.email

	def __unicode__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_superuser

	@models.permalink
	def get_absolute_url(self):
		return ("users:detail", (), {"pk": self.pk})
