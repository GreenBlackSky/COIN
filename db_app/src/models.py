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

TestData = Base.classes.test_data
User = Base.classes.users
Account = Base.classes.accounts
Date = Base.classes.dates
Category = Base.classes.categories
Event = Base.classes.events
Template = Base.classes.templates

session = Session(engine)
