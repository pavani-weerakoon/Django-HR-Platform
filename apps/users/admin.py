from django.contrib import admin
from .models import User, Company, Candidate, Interviewer


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name',
                    'last_name', 'email', 'user_type', 'company_id', 'created_date']


admin.site.register(User, UserAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['owner', 'location', 'company_email']


admin.site.register(Company, CompanyAdmin)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Candidate, CandidateAdmin)


class InterviewerAdmin(admin.ModelAdmin):
    list_display = ['role', 'user']


admin.site.register(Interviewer, InterviewerAdmin)
