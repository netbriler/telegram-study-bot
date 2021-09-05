from datetime import datetime, date

from app import db
from app.models import Task, File
from .files import get_file
from .timetable import get_subject_timetable


def get_task(id: int) -> Task:
    task = Task.query.filter_by(id=id).first()
    return task


def add_task(subject_codename: str, text: str, day: int = 0) -> Task or False:
    days_when_subject = get_subject_timetable(subject_codename)
    if len(days_when_subject) > 0:
        return create_task(text, days_when_subject[day]['date'], subject_codename)
    return False


def create_task(text: str, _date: date, subject_codename: str, files: list = None) -> Task:
    task = Task(text=text, date=_date, subject_codename=subject_codename)

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

        task.files = files_list

    try:
        db.session.add(task)
        db.session.commit()
    except:
        db.session.rollback()

    return task


def edit_task(id: int, text: str = None, _date: date = None, subject_codename: str = None,
              files: list = None) -> Task or False:
    task = get_task(id)
    if not task:
        return False

    if text:
        task.text = text
    if _date:
        task.date = _date
    if subject_codename:
        task.subject_codename = subject_codename
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

        task.files = files_list

    try:
        db.session.commit()
    except:
        db.session.rollback()

    return task


def delete_task(id: int) -> Task or False:
    task = get_task(id)
    if not task:
        return False

    try:
        db.session.delete(task)
        db.session.commit()
    except:
        db.session.rollback()

    return task


def get_tasks() -> list[Task]:
    tasks = Task.query.all()
    return tasks


def get_active_tasks() -> list[Task]:
    tasks = Task.query.filter(Task.date >= date.today())
    return tasks


def get_tasks_by_date(date_to_query: date) -> list[Task]:
    tasks = Task.query.filter_by(date=date_to_query)
    return tasks if tasks.count() else []


def get_tasks_between_date(date_start: date, date_end: date) -> list[Task]:
    tasks = Task.query.filter(Task.date.between(date_start, date_end)).all()
    return tasks


def get_tasks_between_created_date(date_start: datetime, date_end: datetime) -> list[Task]:
    tasks = Task.query.filter(Task.created_at.between(date_start, date_end)).all()
    return tasks


def get_tasks_by_week(week: int, year: int = datetime.now().year) -> list[list[Task]]:
    tasks_list = []
    for i in range(7):
        task_date = date.fromisocalendar(year, week, i + 1)
        tasks_list.append(get_tasks_by_date(task_date))

    return tasks_list
