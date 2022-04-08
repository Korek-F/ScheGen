from django import forms 
from .models import SchoolModel, ClassModel, TeacherModel, LessonModel

class SchoolForm(forms.ModelForm):
    class Meta:
        model = SchoolModel
        fields = [
            "name"
        ]