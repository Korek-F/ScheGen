from django.db import models
from django.contrib.auth.models import User
import jsonfield
# Create your models here.
class SchoolModel(models.Model):
    name = models.CharField(max_length=220)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_json = models.CharField(max_length=9000000000000)
    def __str__(self):
        return self.name
    
class ClassModel(models.Model):
    name = models.CharField(max_length=220)
    school = models.ForeignKey(SchoolModel, on_delete=models.CASCADE )
    avaiable_hours = models.ManyToManyField(to="genApp.TeacherAvaiableHour", related_name="class_model")
    def __str__(self):
        return self.name

class TeacherModel(models.Model):
    name = models.CharField(max_length=220)
    school = models.ForeignKey(SchoolModel, on_delete=models.CASCADE )
    avaiable_hours = models.ManyToManyField(to="genApp.TeacherAvaiableHour", related_name="teacher_model")
    def __str__(self):
        return self.name

class LessonModel(models.Model):
    subject = models.CharField(max_length=220)
    techer = models.ForeignKey(TeacherModel, on_delete=models.CASCADE )
    school_class = models.ForeignKey(ClassModel, on_delete=models.CASCADE )

    def __str__(self):
        return self.school_class.name+ " | "+ self.subject + " | " + self.techer.name

    
class TeacherAvaiableHour(models.Model):
    time = models.IntegerField()

    def __str__(self):
        return str(self.time)

    