from django.db import models

class TestReport(models.Model):
    project_name = models.CharField(max_length=200)
    build_id = models.IntegerField()
    performance_report = models.FileField(upload_to='uploads/%Y/%m/%d/')
    automated_testing_report = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
