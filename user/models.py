from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not password:
            raise ValueError('Password is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Хеширует пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)  # Для активации/деактивации
    is_staff = models.BooleanField(default=False)  # Для доступа к админке

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Поле для логина
    REQUIRED_FIELDS = []  # Дополнительные обязательные поля (пусто)

    def __str__(self):
        return self.username