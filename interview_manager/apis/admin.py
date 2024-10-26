from django.contrib import admin
from .models import Interview

class InterviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'interviewee', 'date', 'time', 'role', 'interviewer', 'job_title', 'department']
    list_filter = ['date', 'role', 'department']
    search_fields = ['interviewee', 'interviewer', 'job_title', 'business_area', 'department']
    ordering = ['date', 'time']
    actions = ['delete_selected']

admin.site.register(Interview, InterviewAdmin)
