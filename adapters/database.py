from sqlalchemy import Column, ForeignKey, Integer, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from adapters.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


sanatorium_tags = Table(
    "sanatorium_tags",
    Base.metadata,
    Column("sanatorium_id", Integer, ForeignKey("sanatoriums.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
profile_tags = Table(
    "profile_tags",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
