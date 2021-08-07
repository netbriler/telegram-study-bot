from datetime import datetime, date
from typing import List

from app import db
from app.models import Task

from .timetable import get_subject_timetable


def get_task(id: int) -> Task:
    task = Task.query.filter_by(id=id).first()
    return task


def add_task(subject_codename: str, text: str, day: int = 0) -> Task or False:
    task = Task(subject_codename=subject_codename, text=text,
                date=get_subject_timetable(subject_codename)[day]['date'])

    db.session.add(task)
    db.session.commit()

    return task


def edit_task(id: int, text: str) -> Task or False:
    task = get_task(id)
    if not task:
        return False

    task.text = text
    db.session.commit()

    return task


def delete_task(id: int) -> Task or False:
    task = get_task(id)
    if not task:
        return False

    db.session.delete(task)
    db.session.commit()

    return task


def get_tasks() -> List[Task]:
    tasks = Task.query.all()
    return tasks


def get_active_tasks() -> List[Task]:
    tasks = Task.query.filter(Task.date >= date.today())
    return tasks


def get_tasks_by_date(date_to_query: date) -> List[Task]:
    tasks = Task.query.filter_by(date=date_to_query)
    return tasks if tasks.count() else []


def get_tasks_by_week(week: int, year: int = datetime.now().year) -> List[List[Task]]:
    tasks_list = []
    for i in range(5):
        task_date = date.fromisocalendar(year, week, i + 1)
        tasks_list.append(get_tasks_by_date(task_date))

    return tasks_list
