"""Data base models."""

import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


connection_string = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ["POSTGRES_USER"],
    os.environ["POSTGRES_PASSWORD"],
    os.environ["POSTGRES_HOST"],
    os.environ["POSTGRES_PORT"],
    os.environ["POSTGRES_DB"],
)

Base = automap_base()
engine = create_engine(connection_string)
Base.prepare(engine, reflect=True)

AccountModel = Base.classes.accounts
SavePointModel = Base.classes.save_points
EventModel = Base.classes.events
CategoryModel = Base.classes.categories

session = Session(engine)
