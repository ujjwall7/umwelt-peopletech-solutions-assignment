from django.contrib import admin
from .models import *

@admin.register(Enrollee)
class EnrolleeAdmin(admin.ModelAdmin):
    list_display = ('id', 'enrollee_id', 'city', 'gender', 'education_level', 'experience', 'company_size', 'target')
    search_fields = ('enrollee_id', 'city', 'gender')
    list_filter = ('gender', 'education_level', 'company_size', 'target')
    ordering = ('enrollee_id',)












