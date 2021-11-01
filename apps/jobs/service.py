
from apps.jobs.models import Question


def get_question_for_job(job):
    question = job.questions.all()
    return question
