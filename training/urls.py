from django.urls import path
from . import views

urlpatterns = [
    path('my-courses/', views.my_courses, name='my_courses'),
    path("upload/<int:course_id>/", views.upload_certificate, name="upload_certificate"),
    path('certificate/download/<int:certificate_id>/', views.download_certificate, name='download_certificate'),
    path("certificate/delete/<int:certificate_id>/", views.delete_certificate, name="delete_certificate"),


    
]