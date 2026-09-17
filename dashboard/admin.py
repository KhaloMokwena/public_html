from django.contrib import admin
from .models import Service, JobPosting, Faq

# This instantly gives you full CRUD (Create, Edit, Delete) for these tables 
# at http://localhost:8000/admin/
admin.site.register(Service)
admin.site.register(JobPosting)
admin.site.register(Faq)