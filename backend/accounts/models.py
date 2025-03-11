from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.role = 'ADMIN'
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('AUTHOR', 'Author'),
        ('EDITOR', 'Editor'),
        ('ADMIN', 'Admin'),
    ]
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # For Django admin access
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Session for {self.user.email}"