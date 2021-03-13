from flask import Blueprint

main = Blueprint('main', __name__)

from . import auth
from . import bot
from . import frontend
