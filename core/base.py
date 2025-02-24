from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db import models
from django.db.models import Manager, QuerySet


class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class AppManager(Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db).exclude(is_deleted=True)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not username:
            raise ValueError('User must have an username address.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Create and return a new superuser."""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        user.role = 'admin'

        return user

class SoftDelete(models.Model):

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()


class User(AbstractBaseUser, PermissionsMixin):
    
    """User in the system."""
    ROLE_CHOICES = (
        ('admin', 'СуперАдмин'),
        ('user', 'Менеджер'),
    )
    role = models.CharField(max_length=20, null = True, blank=True, default = 'user', choices = ROLE_CHOICES)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return f"{self.username} - {self.name}"


class ActivityLog(models.Model):
    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = "Логлар"

    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the log is created
    object_id = models.PositiveIntegerField(null=True, blank=True)  # ID of the affected object, if applicable
    object_type = models.CharField(max_length=100, null=True, blank=True)  # The model name or type of the affected object
    description = models.TextField(null=True, blank=True)  # Optional details about the activity
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Store the user's IP address if necessary

    def __str__(self):
        return f'{self.user} - {self.action} at {self.timestamp}'

class AuditableModel(models.Model):
    """Common auditable model"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        related_name='created_%(class)s_set',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    updated_by = models.ForeignKey(
        User, 
        related_name='updated_%(class)s_set',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def save(self, *args, **kwargs):
        # Check if the object is being created or updated
        if self.pk is None:
            action = 'create'
        else:
            action = 'update'

        # Save the object
        request = kwargs.pop('request', None)
        user = None
        remote_addr = None
        if request:
            user = request.user
            if action == 'create':
                self.created_by = user
            else:
                self.updated_by = user
            remote_addr = request.META.get('REMOTE_ADDR')

        super().save(*args, **kwargs)
        # Log the action
        ActivityLog.objects.create(
            user=user,  # Pass request from view
            action=action,
            object_id=self.pk,
            object_type=self.__class__.__name__,
            description=f'{self.__class__.__name__} {action}',
            ip_address=remote_addr
        )

    def delete(self, *args, **kwargs):
        request = kwargs.pop('request', None)

        user = None
        remote_addr = None
        if request:
            user = request.user
            remote_addr = request.META.get('REMOTE_ADDR')
        # Log the delete action
        ActivityLog.objects.create(
            user=user,  # Pass request from view
            action='delete',
            object_id=self.pk,
            object_type=self.__class__.__name__,
            description=f'{self.__class__.__name__} deleted',
            ip_address=remote_addr
        )
        # Delete the object
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True

