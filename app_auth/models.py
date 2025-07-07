import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.expressions import F
from django.core.validators import MaxValueValidator, MinValueValidator

from mixins.model_mixins.timestamp import TimeStampMixin 
from scraping_project.settings import MEDIA_URL

#  import project constant
from scraping_project.project_constant import SCRAP_USERS, DIRECTORY









# Create your models here.
### --------------------------------------------------------------------------- ###
### AUTH USER MODELS
### --------------------------------------------------------------------------- ###
class Status(models.Model):
    """ 
        Purpose: user status : APPROVED | PENDING | REJECTED 
    """

    name = models.CharField('name of status', max_length=32) 

    def __str__(self):

        return f'{self.name}'

    class Meta:
        verbose_name = "Scrap User Status"
        verbose_name_plural = "Scrap User Status" 



### --------------------------------------------------------------------------- ###
### USER ROLE MODELS
### --------------------------------------------------------------------------- ###
class Role(models.Model):
    """ 
        Purpose: create Roles table
    """

    name = models.CharField('name of role', max_length=512) 

    def __str__(self):

        return f'{self.name}' 

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles" 

        
class AccountManager(BaseUserManager):
    """ Create general and super users """

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, name, password, **extra_fields)




def upload_profile_image(instance, filename):
    return DIRECTORY['user_authentication']['profile_pic'] + f"{filename}"

class ScrapUser(AbstractBaseUser):
    name = models.CharField('name of user', max_length=1024)
    email = models.EmailField('email address', max_length=191, unique=True)
    date_joined = models.DateTimeField('user creation date', auto_now_add=True)

    is_admin = models.BooleanField('is a admin', default=False)
    is_staff = models.BooleanField('is a staff', default=False)
    is_superuser = models.BooleanField('if a superuser', default=False)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='scrap_user_status_type',
        default=2
    )
    device_id = models.CharField('ID of device', max_length=512, null=True, blank=True)
    reset_code = models.CharField(
        'password reset code', max_length=32,
        null=True, blank=True, default=None, editable=False
    )
    profile_image = models.FileField(
        'profile image path', upload_to=upload_profile_image,
        null=True, blank=True
    )
    role = models.ManyToManyField(Role, through='RoleConfiguration', blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin

    def __str__(self):
        return f"{self.name} // {self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=['email'], name='scr_usr_email_idx'),
        ]


class PendingUser(ScrapUser):

    class Meta:
        proxy = True
        verbose_name = "Pending User"
        verbose_name_plural = "Pending Users"



### --------------------------------------------------------------------------- ###
### USER ROLE CONFIGURATION MODELS
### --------------------------------------------------------------------------- ###
class RoleConfiguration(models.Model):
    """ 
        Purpose: create Role Configuration table
    """

    user = models.ForeignKey(
        ScrapUser, on_delete=models.CASCADE, null=True, blank=True, 
        related_name='user_role_conf_fk',
        limit_choices_to={'status': SCRAP_USERS['status']['APPROVED']}
    ) 
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):

        return f'{self.user.name}/{self.role.name}' 

    class Meta:
        verbose_name = "Role Configuration"
        verbose_name_plural = "Role Configurations" 



