import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import ForeignKey, Table, Column, Integer

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/sanat")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

sanatorium_tags = Table("sanatorium_tags", Base.metadata,
                            Column("sanatorium_id", Integer, ForeignKey("sanatoriums.id"), primary_key=True),
                            Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
                            )
profile_tags = Table("profile_tags", Base.metadata,
                            Column("profile_id", Integer, ForeignKey("profiles.id"), primary_key=True),
                            Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
                            )