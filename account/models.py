from django.db import models
from donation.models import Profile
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )

        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.email)+str("-------")+str(self.username)
    @property
    def profile(self):
        return self.profile_set.all()

# class Friends(models.Model):
#     user = models.OneToOneField(
#         AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     friends = models.ManyToManyField(AUTH_USER_MODEL, blank=True)

#     def __str__(self):
#         return self.user.get_full_name


# class Friend_Request(models.Model):
#     from_user = models.ForeignKey(
#         AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE, null=True)
#     to = models.ForeignKey(
#         AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE, null=True)
