
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Assignment(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('REVIEW', 'Needs Review'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.employee.username} - {self.course.name}"


# # 3. Certificate model → Employee uploads certificate after course
# class Certificate(models.Model):
#     assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)  
#     file = models.FileField(upload_to='certificates/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     ocr_text = models.TextField(blank=True, null=True)  # For storing extracted text
#     verification_score = models.FloatField(default=0.0) # AI/Fuzzy matching score

#     def __str__(self):
#         return f"Certificate for {self.assignment}"



class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="certificates", null=True, blank=True)

    file = models.CharField(max_length=255, blank=True, null=True)  # Google Drive file ID
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"



