from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Slot(models.Model):
    CATEGORY_CHOICES = [
        ('design', 'Design'),
        ('development', 'Development'),
        ('embroidery', 'Embroidery'),
        ('qa', 'QA'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    request_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='slots')
    team_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='lead_slots'
    )
    developers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='assigned_slots', blank=True
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='requested_slots'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_slots'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'slots'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_id} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.request_id:
            import datetime
            year = datetime.date.today().year
            last = Slot.objects.filter(
                request_id__startswith=f"SLT-{year}-"
            ).order_by('request_id').last()
            if last:
                num = int(last.request_id.split('-')[-1]) + 1
            else:
                num = 1
            self.request_id = f"SLT-{year}-{num:05d}"
        super().save(*args, **kwargs)
