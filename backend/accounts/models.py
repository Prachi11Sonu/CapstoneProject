
# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class User(AbstractUser):

#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", "Admin"
#         TENDER_MANAGER = "TENDER_MANAGER", "Tender Manager"
#         BIDDER = "BIDDER", "Bidder"
#         REVIEWER = "REVIEWER", "Reviewer"

#     # Email must be unique for every user
#     email = models.EmailField(unique=True)

#     # Phone number of the user
#     phone_number = models.CharField(max_length=15)

#     # User's role in the platform
#     role = models.CharField(
#         max_length=20,
#         choices=Role.choices,
#         default=Role.BIDDER,
#     )

#     # Use email instead of username for login
#     username = None

#     USERNAME_FIELD = "email"

#     REQUIRED_FIELDS = ["first_name", "last_name"]

#     def __str__(self):
#         return f"{self.email} ({self.role})"

















from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TENDER_MANAGER = "TENDER_MANAGER", "Tender Manager"
        BIDDER = "BIDDER", "Bidder"
        REVIEWER = "REVIEWER", "Reviewer"

    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.BIDDER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

