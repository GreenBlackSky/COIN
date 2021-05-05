"""Data base models."""

import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


connection_string = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ['POSTGRES_USER'],
    os.environ['POSTGRES_PASSWORD'],
    os.environ['POSTGRES_HOST'],
    os.environ['POSTGRES_PORT'],
    os.environ['POSTGRES_DB'],
)

Base = automap_base()
engine = create_engine(connection_string)
Base.prepare(engine, reflect=True)

UserModel = Base.classes.users
AccountModel = Base.classes.accounts
CategoryModel = Base.classes.labels
EventModel = Base.classes.events
TemplateModel = Base.classes.templates

session = Session(engine)
