from django.contrib import admin

# Register your models here.


from .models import Question, Job, Section, Candidateship, Interview, Experience

admin.site.register(Question)
admin.site.register(Job)
admin.site.register(Section)
admin.site.register(Candidateship)
admin.site.register(Interview)
admin.site.register(Experience)
