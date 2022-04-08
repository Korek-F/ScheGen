from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework import serializers
from .models import SchoolModel, TeacherModel, LessonModel, ClassModel, TeacherAvaiableHour
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SchoolForm
from django.shortcuts import get_object_or_404
from .serializers import SchoolModelSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .generator import generate_schedule
import json

# Create your views here.
def MainPage(request):
    return render(request, "genApp/main_page.html")

class SchoolsListView(LoginRequiredMixin,ListView):
    model = SchoolModel
    template_name = "genApp/schools_list_view.html"
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class SchoolDetailView(LoginRequiredMixin, DetailView):
    model = SchoolModel
    template_name = "genApp/school_detail_view.html"

class ClassDetailView(LoginRequiredMixin, DetailView):
    model = ClassModel
    template_name = "genApp/class_detail_view.html"

class SchoolCreateView(LoginRequiredMixin, CreateView):
    model = SchoolModel
    form_class = SchoolForm
    template_name = "genApp/school_create_view.html"
    success_url = reverse_lazy('school_list_view')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.owner = self.request.user
        f.save()
        return super().form_valid(form)

class SchoolDeleteView(DeleteView):
    model = SchoolModel
    success_url = reverse_lazy('school_list_view')

def add_class(request,school_id):
    if request.method == "POST":
        school = get_object_or_404(SchoolModel, pk=school_id)
        new_class_name = request.POST["new_class_name"]
        new_class = ClassModel.objects.create(school=school, name=new_class_name)
        for i in TeacherAvaiableHour.objects.all():
            new_class.avaiable_hours.add(i)
        return redirect('school_detail_view', pk=school.id)

def add_teacher(request,school_id):
    if request.method == "POST":
        school = get_object_or_404(SchoolModel, pk=school_id)
        new_teacher_name = request.POST["new_teacher_name"]
        new_teacher = TeacherModel.objects.create(school=school, name=new_teacher_name)
        return redirect('school_detail_view', pk=school.id)

class ClassDeleteView(DeleteView):
    model = ClassModel
    
    def get_success_url(self):
        class_model = self.object
        return reverse_lazy( 'school_detail_view', kwargs={'pk': class_model.school.id})

class TeacherDeleteView(DeleteView):
    model = TeacherModel
    
    def get_success_url(self):
        teacher_model = self.object
        return reverse_lazy( 'school_detail_view', kwargs={'pk': teacher_model.school.id})

def add_lesson(request, class_id):
    if request.method == "POST":
        teacher_id = request.POST["teacher"]
        subject = request.POST["subject"]
        teacher = get_object_or_404(TeacherModel, pk=int(teacher_id))
        school_class = get_object_or_404(ClassModel, pk=int(class_id))
        LessonModel.objects.create(subject=subject, techer=teacher, school_class=school_class)
        return redirect('class_detail_view', pk=class_id)

class LessonDeleteView(DeleteView):
    model = LessonModel
    
    def get_success_url(self):
        lesson_model= self.object
        return reverse_lazy( 'class_detail_view', kwargs={'pk': lesson_model.school_class.id})

class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = TeacherModel
    template_name = "genApp/teacher_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        context["hours"] = TeacherAvaiableHour.objects.all().order_by('time')
        return context

def change_teacher_available_hours(request, teacher_id):
    if request.method == "POST":
        checked_hours = request.POST.getlist('checks')
        teacher = get_object_or_404(TeacherModel, pk=teacher_id)
        teacher.avaiable_hours.clear()
        for i in checked_hours:
            hour = TeacherAvaiableHour.objects.get(time=int(i))
            teacher.avaiable_hours.add(hour)
    return redirect('teacher_detail_view', pk=teacher_id)

#@api_view(['GET'])
def school_schedule_generator(request,pk):
    queryset = SchoolModel.objects.all().get(pk=pk)
    if(request.user == queryset.owner):
        serializer = SchoolModelSerializer(queryset, many=False)
       
        #if True:
        #    return Response(serializer.data)
        schedule = generate_schedule(serializer.data)
        context = {
            "schedule":json.dumps(schedule)
        }
        queryset.schedule_json = json.dumps(schedule)
        queryset.save()
        return render(request, "genApp/generated_schedule.html", context)
    return redirect('open_school_schedule', pk=pk)

def open_school_schedule(request,pk):
    queryset = SchoolModel.objects.all().get(pk=pk)
    context = {
        "schedule":queryset.schedule_json
    }
    return render(request, "genApp/generated_schedule.html", context)