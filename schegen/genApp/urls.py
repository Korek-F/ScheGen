from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage, name="main"),
    path('school-list/', views.SchoolsListView.as_view(), name="school_list_view"),
    path('school/<int:pk>', views.SchoolDetailView.as_view(), name="school_detail_view"),
    path('class/<int:pk>', views.ClassDetailView.as_view(), name="class_detail_view"),
    path('teacher/<int:pk>', views.TeacherDetailView.as_view(), name="teacher_detail_view"),
    path('create-school', views.SchoolCreateView.as_view(), name="school_create_view"),
    path('delete-school/<int:pk>', views.SchoolDeleteView.as_view(), name="school_delete_view"),
    path('add-class/<int:school_id>', views.add_class, name="add_class"),
    path('add-teacher/<int:school_id>', views.add_teacher, name="add_teacher"),
    path('add-lesson/<int:class_id>', views.add_lesson, name="add_lesson"),
    path('delete-class/<int:pk>', views.ClassDeleteView.as_view(), name="class_delete_view"),
    path('delete-teacher/<int:pk>', views.TeacherDeleteView.as_view(), name="teacher_delete_view"),
    path('delete-lesson/<int:pk>', views.LessonDeleteView.as_view(), name="lesson_delete_view"),
    path('change-teacher-available-hours/<int:teacher_id>', views.change_teacher_available_hours, name="change_teacher_available_hours"),
    path('school-schedule-generator/<int:pk>', views.school_schedule_generator, name="school_schedule_generator"),
    path('open-school-schedule/<int:pk>', views.open_school_schedule, name="open_school_schedule"),
]