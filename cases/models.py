from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse

CRIME_TYPE_CHOICES = [
    ('Phishing','Phishing'),
    ('Identity Theft','Identity Theft'),
    ('Online Fraud','Online Fraud'),
    ('Hacking','Hacking'),
    ('Cyberstalking','Cyberstalking'),
    ('Malware/Ransomware','Malware/Ransomware'),
    ('Others','Others'),
]

STATUS_CHOICES = [
    ('New','New'),
    ('Under Review','Under Review'),
    ('Investigation','Investigation'),
    ('Resolved','Resolved'),
    ('Closed','Closed'),
]

class Case(models.Model):
    TRACKING_PREFIX = "CCMS"
    tracking_id = models.CharField(max_length=30, unique=True, blank=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cases')
    crime_type = models.CharField(max_length=50, choices=CRIME_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    date_of_crime = models.DateField()
    victim_name = models.CharField(max_length=255)
    description = models.TextField()
    evidence_image = models.ImageField(upload_to='evidence/%Y/%m/%d/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            suffix = get_random_string(6).upper()
            self.tracking_id = f"{self.TRACKING_PREFIX}-{suffix}"
            while Case.objects.filter(tracking_id=self.tracking_id).exists():
                suffix = get_random_string(6).upper()
                self.tracking_id = f"{self.TRACKING_PREFIX}-{suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tracking_id or 'Case'

    def get_absolute_url(self):
        return reverse('case_detail', args=[str(self.pk)])
