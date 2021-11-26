from django.contrib import admin

# Register your models here.


from .models import Question, Job, Section, Candidateship, Interview, Experience


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_type', 'job', 'section']


admin.site.register(Question, QuestionAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ['role', 'salary', 'company_id']


admin.site.register(Job, JobAdmin)
admin.site.register(Section)


class CandidateshipAdmin(admin.ModelAdmin):
    list_display = ['candidate_id', 'job']


admin.site.register(Candidateship, CandidateshipAdmin)


class InterviewAdmin(admin.ModelAdmin):
    list_display = ['interviewer_id', 'candidateship_id']


admin.site.register(Interview, InterviewAdmin)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'worked_place', 'candidate_id']


admin.site.register(Experience, ExperienceAdmin)
