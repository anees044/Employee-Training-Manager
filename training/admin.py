from django.contrib import admin,messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Course, Assignment, Certificate
from django.urls import path
from django.shortcuts import render
from django import forms
from .forms import CourseAdminForm
from django.utils.html import format_html
from django.urls import reverse
from . import views


admin.site.unregister(User)


class EmployeeAdmin(DefaultUserAdmin):
    
    list_display = DefaultUserAdmin.list_display 
    

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('employeestatus/', self.admin_site.admin_view(self.employee_status_view), name='employee-status'),
            path('employeestatus/<int:user_id>/',self.admin_site.admin_view(self.employee_detail_view),name='employee-detail'),
            path("certificate/download/<int:certificate_id>/", views.download_certificate, name="download_certificate"),
            
        ]
        return custom_urls + urls

    
    def employee_status_view(self, request):
        employee_group = Group.objects.get(name="Employee")
        employees = User.objects.filter(groups=employee_group)
        context = {'employees': employees, 'title': 'Employees Dashboard'}
        return render(request, 'admin/employee_status.html', context)
    
    def employee_detail_view(self, request, user_id):
        employee = User.objects.get(id=user_id)
        assignments = Assignment.objects.filter(employee=employee)
        certificates = Certificate.objects.filter(user=employee)
        context = {
            'employee': employee,
            'assignments': assignments,
            'certificates': certificates,
        }
        return render(request, 'admin/employee_detail.html', context)


admin.site.register(User, EmployeeAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'course', 'status', 'assigned_at')
    list_filter = ('status', 'course')
    search_fields = ('employee__username', 'course__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            
            kwargs["queryset"] = User.objects.filter(groups__name="Employee")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "uploaded_at", "file")
    list_filter = ("uploaded_at",)
    search_fields = ("user__username", "course__name")
    readonly_fields = ("user", "course", "uploaded_at")

    
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ("id", "name", "created_at")

    class Media:
        js = ("admin/js/assign_all.js",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        assign_all = form.cleaned_data.get("assign_all")
        employees = form.cleaned_data.get("employees")

        if assign_all:
            employees = User.objects.filter(groups__name="Employee")

        created_count = 0
        for emp in employees:
            _, created = Assignment.objects.get_or_create(
                employee=emp,
                course=obj,
                defaults={"status": "PENDING"}
            )
            if created:
                created_count += 1

        messages.success(
            request,
            f"Course '{obj.name}' assigned to {created_count} employees."
        )



admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Certificate, CertificateAdmin)



    



