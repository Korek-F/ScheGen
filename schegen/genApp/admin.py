from django.contrib import admin
from .models import ClassModel, SchoolModel, TeacherModel, LessonModel, TeacherAvaiableHour
# Register your models here.
admin.site.register(ClassModel)
admin.site.register(SchoolModel)
admin.site.register(TeacherModel)
admin.site.register(LessonModel)
admin.site.register(TeacherAvaiableHour)