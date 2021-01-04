from fuzzywuzzy import fuzz

from app.models import Subject


def get_subject(codename: str) -> Subject:
    subject = Subject.query.filter_by(codename=codename).first()
    return subject


def get_all_subjects() -> list[Subject]:
    subjects = Subject.query.all()
    return sorted(subjects, key=lambda k: k.name.lower())


def get_none_subject() -> Subject:
    return Subject(
        codename='None',
        name='Нету пары',
        _aliases=''
    )


def recognize_subject(subject_to_recognize: str) -> Subject:
    most_suitable_subject = get_none_subject()
    max_recognize_percent = 0.00

    for subject in get_all_subjects():

        for aliases in subject.aliases:
            current_recognize_percent = fuzz.ratio(subject_to_recognize, aliases)

            # If the percentage of matches is greater, then we have a new most suitable subject
            if current_recognize_percent > max_recognize_percent:
                most_suitable_subject = subject
                max_recognize_percent = current_recognize_percent

    return most_suitable_subject
