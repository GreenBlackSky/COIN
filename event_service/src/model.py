"""Data base models."""

import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


connection_string = "postgresql://{}:{}@{}:{}/event_db".format(
    os.environ['POSTGRES_USER'],
    os.environ['POSTGRES_PASSWORD'],
    os.environ['POSTGRES_HOST'],
    os.environ['POSTGRES_PORT'],
)

Base = automap_base()
engine = create_engine(connection_string)
Base.prepare(engine, reflect=True)

EventModel = Base.classes.events

session = Session(engine)
