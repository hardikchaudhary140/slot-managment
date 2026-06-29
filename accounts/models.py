from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr', 'HR Department'),
        ('team_lead', 'Team Lead'),
        ('developer', 'Developer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')
    team = models.ForeignKey('slots_app.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    phone = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
