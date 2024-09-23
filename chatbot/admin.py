from django.contrib import admin
from .models import Course
from import_export.admin import ImportExportModelAdmin

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ('teacher_name','course_name')