from html import escape

from fuzzywuzzy import fuzz

from app import db
from app.models import Subject, File
from .files import get_file


def get_subject(codename: str) -> Subject:
    subject = Subject.query.filter_by(codename=codename).first()
    return subject


def create_subject(codename: str, name: str, aliases: str or list = None,
                   info: str = None, teacher: str = None, audience: str = None, files: list = None, *args,
                   **kwargs) -> Subject or False:
    subject = Subject(codename=codename)

    subject.name = escape(name)
    subject.aliases = aliases
    subject.info = info
    subject.teacher = escape(teacher)
    subject.audience = escape(audience)

    if files or type(files) == list:
        files_list = list()
        for file in files:
            if 'id' in file:
                file_model = get_file(file['id'])
                file_model.title = file['title']
                file_model.file_id = file['file_id']
            else:
                file_model = File(title=file['title'], file_id=file['file_id'])

            files_list.append(file_model)

        subject.files = files_list

    try:
        db.session.add(subject)
        db.session.commit()
    except:
        db.session.rollback()

    return subject


def edit_subject(codename: str, name: str, aliases: str or list = None,
                 info: str = None, teacher: str = None, audience: str = None, files: list = None, *args,
                 **kwargs) -> Subject or False:
    subject = get_subject(codename)
    if not subject:
        return False

    subject.name = escape(name)
    subject.aliases = aliases
    subject.info = info
    subject.teacher = escape(teacher)
    subject.audience = escape(audience)

    if files or type(files) == list:
        files_list = list()
        for file in files:
            if 'id' in file:
                file_model = get_file(file['id'])
                file_model.title = escape(file['title'])
                file_model.file_id = file['file_id']
            else:
                file_model = File(title=escape(file['title']), file_id=file['file_id'])

            files_list.append(file_model)

        subject.files = files_list

    try:
        db.session.commit()
    except:
        db.session.rollback()

    return subject


def delete_subject(codename: str):
    subject = get_subject(codename)
    if not subject:
        return False

    try:
        db.session.delete(subject)
        db.session.commit()
    except:
        db.session.rollback()

    return True


def get_all_subjects() -> list[Subject]:
    subjects = Subject.query.all()
    return sorted(subjects, key=lambda k: k.name.lower())


def get_none_subject() -> Subject:
    return Subject(
        codename='None',
        name='Нет пары',
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
