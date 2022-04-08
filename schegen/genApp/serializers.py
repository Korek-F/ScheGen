from .models import SchoolModel, TeacherModel, ClassModel, LessonModel, TeacherAvaiableHour
from rest_framework import serializers

class LessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = ('id', 'subject','techer', 'school_class')

class TeacherAvaiableHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAvaiableHour
        fields = ('time',)

class TeacherModelSerializer(serializers.ModelSerializer):
    avaiable_hours = TeacherAvaiableHourSerializer(many=True)
    class Meta:
        model = TeacherModel
        fields = ('id', 'name', 'avaiable_hours')

class ClassModelSerializer(serializers.ModelSerializer):
    lessonmodel_set = LessonModelSerializer(many=True)
    avaiable_hours = TeacherAvaiableHourSerializer(many=True)
    class Meta:
        model = ClassModel
        fields = ('id', 'name', 'avaiable_hours', 'lessonmodel_set')

class SchoolModelSerializer(serializers.ModelSerializer):
    classmodel_set = ClassModelSerializer(many=True)
    teachermodel_set = TeacherModelSerializer(many=True)
    class Meta:
        model = SchoolModel
        fields = ('id', 'name','classmodel_set', 'teachermodel_set')



