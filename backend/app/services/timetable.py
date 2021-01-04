import datetime
import calendar
from datetime import datetime, timedelta, date

from .subjects import get_none_subject, get_subject

from app.models import Timetable, Subject


def get_subjects_by_date(current_date: date) -> list[Subject] or None:
    day = _get_day_number_by_date(current_date)
    return _get_subjects(day)


def get_subjects_by_week(week, year: int = datetime.now().year):
    subjects_list = []
    for i in range(5):
        subjects_date = datetime.combine(date.fromisocalendar(year, week, i + 1), datetime.min.time()).date()
        subjects_list.append({'name': calendar.day_name[i], 'subjects': get_subjects_by_date(current_date=subjects_date)})

    return subjects_list


def _is_even_week(current_date: date) -> bool:
    """Checks the parity week"""
    verification_date = date(2019, 9, 1)

    monday1 = (verification_date - timedelta(days=verification_date.weekday()))
    monday2 = (current_date - timedelta(days=current_date.weekday()))
    return bool(int((monday2 - monday1).days / 7) % 2)


def _get_day_number_by_date(current_date: date) -> int:
    day = current_date.weekday() + 1
    if _is_even_week(current_date):
        day += 7
    return int(day)


def _get_subjects(day: int) -> list[Subject] or None:
    timetable = Timetable.query.filter_by(id=day).first()

    if not timetable.is_work_day:
        return None

    subjects_list = list()
    subjects = timetable.subjects.split(',')

    for subject in subjects:
        if subject == 'None':
            subjects_list.append(get_none_subject())
        else:
            subjects_list.append(get_subject(subject))
    return subjects_list
