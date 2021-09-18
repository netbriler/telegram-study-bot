from .files import File
from .photo import Photo
from .subjects import Subject
from .tasks import Task
from .timetable import Timetable, init_timetable
from .users import User


def init_models():
    init_timetable()
