from django.contrib import admin # type: ignore
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tracking_id', 'reporter', 'crime_type', 'status',
        'location', 'victim_name', 'date_of_crime', 'created_at'
    )
    list_filter = ('crime_type', 'status', 'date_of_crime')
    search_fields = (
        'tracking_id', 'reporter_email', 'reporter_username',
        'victim_name', 'location', 'crime_type'
    )
    fields = (
        'crime_type', 'description', 'status', 'tracking_id',
        'location', 'victim_name', 'date_of_crime', 'evidence_image'
    )