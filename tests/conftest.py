import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from adapters import orm  # noqa: F401
from adapters.database import Base
from adapters.orm import SanatoriumORM, TagOrm, UserORM, UserProfileORM
from entrypoints import flask_app as flask_app_module
from entrypoints.flask_app import app as flask_app


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    sessiontest = sessionmaker(bind=engine)
    session = sessiontest()

    yield session

    session.close()
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())


@pytest.fixture
def a_user(db_session):
    user_orm = UserORM(name="Сава", login="sava", password="123")
    db_session.add(user_orm)
    db_session.commit()
    return user_orm


@pytest.fixture
def some_tags(db_session):
    tags = [
        TagOrm(name="кардиология", category="medical"),
        TagOrm(name="неврология", category="medical"),
        TagOrm(name="бассейн", category="services"),
        TagOrm(name="wifi", category="conditions"),
    ]
    db_session.add_all(tags)
    db_session.commit()
    return tags


@pytest.fixture
def a_sanatorium(db_session, some_tags):
    sanatorium_orm = SanatoriumORM(
        name="Тестовый санаторий",
        budget=50000,
        region="Крым",
        food="трёхразовое",
        rating=4.5,
        tags=some_tags,
    )
    db_session.add(sanatorium_orm)
    db_session.commit()
    return sanatorium_orm


@pytest.fixture
def a_profile(db_session, a_user, some_tags):
    profile_orm = UserProfileORM(
        user_id=a_user.id,
        goal="лечение",
        budget=5000,
        region="Крым",
        tags=some_tags,
        budget_weight=1,
        region_weight=1,
        medical_weight=1,
        services_weight=1,
        conditions_weight=1,
    )
    db_session.add(profile_orm)
    db_session.commit()
    return profile_orm


@pytest.fixture(scope="session")
def test_session_factory(engine):
    return sessionmaker(bind=engine)


@pytest.fixture
def client(db_session, test_session_factory, engine, monkeypatch):
    monkeypatch.setattr(flask_app_module, "SessionLocal", test_session_factory)

    # тестовый клиент Flask
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
