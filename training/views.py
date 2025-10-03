from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course,Certificate,Assignment
from .forms import CertificateUploadForm
from django.utils import timezone
from  utils.google_drive import upload_file_to_gdrive,get_drive_service,download_file_from_drive
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os,io,ast
from googleapiclient.http import MediaIoBaseDownload
from django.conf import settings
from django.contrib import messages



@login_required
def my_courses(request):
    
    assignments = Assignment.objects.filter(employee=request.user)
    return render(request, "training/my_courses.html", {"assignments": assignments})



def upload_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, course=course, employee=request.user)

    if request.method == "POST":
        form = CertificateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES["file"]

            
            folder_id = "1Pfh-MR0uZJsTq1c9wgjpFM9sK7GEjQjY" 
            drive_file_id = upload_file_to_gdrive(file_obj, file_obj.name, folder_id=folder_id)

            
            
            certificate = Certificate.objects.create(
                user=request.user,
                course=course,
                assignment=assignment,
                file=drive_file_id
            )

            
            assignment.status = "COMPLETED"
            assignment.completed_at = timezone.now()
            assignment.save()

            return redirect("my_courses")
    else:
        form = CertificateUploadForm()

    return render(request, "training/upload.html", {"form": form, "course": course})

def delete_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    if request.method == "POST":
        certificate.delete()  
        messages.success(request, "Certificate deleted. You can upload a new one.")
        return redirect("my_courses")
    return redirect("my_courses")


    

def download_certificate(request, certificate_id):

    cert = get_object_or_404(Certificate, id=certificate_id)

    if not cert.file:
        raise Http404("No file found for this certificate")

    
    file_id = cert.file
    if file_id.startswith("{"):  
        try:
            file_dict = ast.literal_eval(file_id)
            file_id = file_dict.get("id")
        except Exception:
            raise Http404("Invalid file reference in DB")

    file_name, mime_type, file_bytes = download_file_from_drive(file_id)

    resp = HttpResponse(file_bytes, content_type=mime_type)
    resp["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return resp