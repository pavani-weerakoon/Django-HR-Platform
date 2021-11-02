
from apps.jobs.models import Question


def get_question_for_job(job):
    questions = job.questions.all()
    return questions
