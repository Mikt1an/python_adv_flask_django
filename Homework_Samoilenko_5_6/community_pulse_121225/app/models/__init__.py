from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

from .categories import Category
from .responses import Response
from .questions import Question
from .statistics import Statistics


