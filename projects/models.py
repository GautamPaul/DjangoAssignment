from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class Projects(models.Model):  # Projects Model
    name = models.CharField(max_length=100)
    startDate = models.DateField(auto_now_add=True)
    expectedEndDate = models.DateField()


class ResourceManager(BaseUserManager):
    # overriding the create_user function of the BaseUserManager class
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email address is a required field.")
        if not username:
            raise ValueError("Username is a required field.")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # overriding the create_superuser function of the BaseUserManager class
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        # since we are creating a superuser, these parameters will be set to True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Resource(AbstractBaseUser):  # Custom user model for resources
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    # password = models.CharField(max_length=128)
    # all these fields are included in the abstract base user class so these need to be overridden
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # project allocated to the resource
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, default=1)

    # field that will be used to login
    USERNAME_FIELD = 'email'

    # fields that will be necessary to be filled
    REQUIRED_FIELDS = ['username']

    # default return value if none of the fields is accessed
    def __str__(self):
        return self.username

    # permission methods that need to be overridden
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    objects = ResourceManager()


class Release(models.Model):    # Release Model
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    release_date = models.DateField()
    deliverables = models.TextField()
