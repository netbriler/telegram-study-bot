import calendar
import datetime
import re
from datetime import datetime, timedelta, date

from app import db
from app.models import Timetable, Subject
from .subjects import get_none_subject, get_subject


def edit_timetable(id: int, subjects: str):
    day = Timetable.query.filter_by(id=id).first()
    if not day:
        return False

    if not subjects:
        day.is_work_day = False
    else:
        day.is_work_day = True
        day.subjects = subjects

    db.session.commit()

    return True


def get_timetable() -> list[dict[str, [list, any]]]:
    timetable = Timetable.query.all()

    timetable_list = []
    for day in timetable:
        day_name_id = day.id if day.id < 8 else day.id - 7
        day_name = calendar.day_name[day_name_id - 1].capitalize()
        timetable_list.append({
            'day_id': day.id,
            'day_name': day_name,
            'subjects': list(map(lambda s: s.to_json(), _get_subjects(day.id)))
        })

    return timetable_list


def get_subjects_by_date(current_date: date) -> list[Subject] or None:
    day = _get_day_number_by_date(current_date)
    return _get_subjects(day)


def get_subjects_by_week(week: int, year: int = datetime.now().year) -> list[list[Subject]]:
    subjects_list = []
    for i in range(7):
        subjects_date = datetime.combine(date.fromisocalendar(year, week, i + 1), datetime.min.time()).date()
        subjects_list.append(get_subjects_by_date(current_date=subjects_date))

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


def _get_subjects(day: int) -> list[Subject]:
    timetable = Timetable.query.filter_by(id=day).first()

    if not timetable or not timetable.is_work_day or len(timetable.subjects.strip()) < 1:
        return []

    subjects_list = list()
    subjects = timetable.subjects.split(',')

    for subject in subjects:
        if subject == 'None':
            subjects_list.append(get_none_subject())
        else:
            subjects_list.append(get_subject(subject))
    return subjects_list


def get_subject_timetable(subject_codename: str) -> list[dict]:
    """Returns an array with days in the timetable in which the given subject is present"""
    timetable = Timetable.query.filter(Timetable.subjects.like(f'%{subject_codename}%')).all()
    timetable = list(filter(lambda s: re.search(fr'(^|,){subject_codename}', s.subjects), timetable))

    date_now = datetime.now().date()
    current_day = _get_day_number_by_date(date_now)
    days_list = []
    for _day in timetable:
        day = dict()
        day['id'] = int(_day.id)

        if day['id'] > current_day:
            day['days_to'] = day['id'] - current_day
        else:
            day['days_to'] = 14 - current_day + day["id"]

        day['date'] = (date_now + timedelta(days=day['days_to']))
        day['date_string'] = day['date'].strftime('%Y-%m-%d')
        days_list.append(day)
    return sorted(days_list, key=lambda k: k['days_to'])
