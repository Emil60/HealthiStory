from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, passport, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not passport:
            raise ValueError('Provide passport ID')
        user = self.model(passport=passport, **extra_fields)
        user.set_password(password)
        print("password hashed")
        user.save(using=self._db)
        user.is_active = True
        return user

    def create_user(self, passport, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        print("create user")
        return self._create_user(passport, password, **extra_fields)

    def create_superuser(self, passport, password, **extra_fields):
        print("super")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(passport, password, **extra_fields)