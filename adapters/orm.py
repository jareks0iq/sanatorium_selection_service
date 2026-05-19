from adapters.database import Base, sanatorium_tags, profile_tags
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    login: Mapped[str]
    password: Mapped[str]

    profile: Mapped["UserProfileORM"] = relationship(back_populates="user")
    review: Mapped[list["ReviewORM"]] = relationship(back_populates="user")

class UserProfileORM(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    goal: Mapped[str]
    budget: Mapped[int]
    region: Mapped[str]
    budget_weight: Mapped[int]
    region_weight: Mapped[int]
    medical_weight: Mapped[int]
    services_weight: Mapped[int]
    conditions_weight: Mapped[int]

    user: Mapped["UserORM"] = relationship(back_populates="profile")
    tags: Mapped[list["TagOrm"]] = relationship(secondary=profile_tags)

class SanatoriumORM(Base):
    __tablename__ = "sanatoriums"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    budget: Mapped[int]
    region: Mapped[str]
    tags: Mapped[list["TagOrm"]] = relationship(secondary=sanatorium_tags)
    food: Mapped[str]
    rating: Mapped[float]

    review: Mapped[list["ReviewORM"]] = relationship(back_populates="sanatorium")

class TagOrm(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category: Mapped[str]

class ReviewORM(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sanatorium_id: Mapped[int] = mapped_column(ForeignKey("sanatoriums.id"))
    text: Mapped[str]
    rating: Mapped[float]
    created_at: Mapped[str]

    user: Mapped["UserORM"] = relationship(back_populates="review")
    sanatorium: Mapped["SanatoriumORM"] = relationship(back_populates="review")

