from apps.users.models import Candidate
from apps.jobs.serializers import SectionSerializer, QuestionSerializer


def add_cantidate_to_job(candidate_ids, job):
    candidate_users = []
    candidates = []
    for candidate_id in candidate_ids:
        candidate = Candidate.objects.get(id=candidate_id)
        candidates.append(candidate)
        job.candidates.add(candidate)

    for candidate in candidates:
        candidate_users.append(candidate.user)
    return candidate_users


def add_questions(data, job):
    all_questions = []
    for dic in data:
        data_question = dic['question_type']
        data_section = dic['section']
        sec_dict = {"section_name": data_section}
        questions = []

        for x in data_question:
            questions.append({"question_type": x})

        section_serializer = SectionSerializer(data=sec_dict)
        if section_serializer.is_valid(raise_exception=True):
            sections = section_serializer.save()

        question_serializer = QuestionSerializer(
            data=questions, many=True)
        if question_serializer.is_valid(raise_exception=True):
            ques = question_serializer.save(
                job=job, section=sections)
            all_questions.append(ques)

    flat_list = []
    for sublist in all_questions:
        for item in sublist:
            flat_list.append(item)
    return flat_list
