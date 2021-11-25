from django.contrib import admin
from .models import User, Company, Candidate, Interviewer


# Register your models here.

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Candidate)
admin.site.register(Interviewer)
