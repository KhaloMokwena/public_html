from django.contrib import admin
from .models import Record, Service, JobPosting, Faq, Division, ContactMessage, ContentBlock, JobApplication

# The friendlier editor lives at http://localhost:8000/manage/ ; these stay available as a fallback.
admin.site.register(Record)
admin.site.register(Service)
admin.site.register(JobPosting)
admin.site.register(Faq)
admin.site.register(Division)
admin.site.register(ContactMessage)
admin.site.register(ContentBlock)
admin.site.register(JobApplication)
