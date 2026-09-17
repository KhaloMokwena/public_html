from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, help_text="e.g., IT Services, Media, Construction")
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="Optional bootstrap icon class")
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.category}: {self.title}"

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Hybrid (Centurion based)")
    level = models.CharField(max_length=100, help_text="e.g., Senior, Junior (Internship)")
    scope = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question