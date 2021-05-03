from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

def upload_location(instance, filename):
    file_path = 'profile/{username}/{file_name}'.format(username=str(instance.username), file_name=filename)
    return file_path

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users should have email")
        if not username:
            raise ValueError("Users should have username")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password
        )
        is_admin                    = models.BooleanField(default=True)
        is_staff                    = models.BooleanField(default=True)
        is_superuser                = models.BooleanField(default=True)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    email                       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                    = models.CharField(max_length=30, unique=True)
    avatar                      = models.ImageField(upload_to=upload_location,default='avatar/default.png', blank=False)
    date_joined                 = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                  = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email + ", " + self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
