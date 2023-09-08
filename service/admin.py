from django.contrib import admin

# Register your models here.
from service.models import UserProfile


@admin.register(UserProfile)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id','user')