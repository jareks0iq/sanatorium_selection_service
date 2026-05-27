from adapters.repository import ReviewRepository, SanatoriumRepository, UserRepository
from domain.model import Review, User, UserProfile


def test_add_and_get_user(db_session):
    repo = UserRepository(db_session)
    user = User(id=None, name="Иван", login="ivan", password="secret")

    repo.add(user)

    assert user.id is not None

    fetched = repo.get_by_login("ivan")
    fetched2 = repo.get_by_id(user.id)
    assert fetched is not None
    assert fetched2 is not None
    assert fetched.name == fetched2.name == "Иван"
    assert fetched.login == fetched2.login == "ivan"


def test_update_password_with_correct_old_password_changes_it(db_session):
    repo = UserRepository(db_session)
    user = User(id=None, name="Сава", login="sava", password="123")
    repo.add(user)

    right_password = repo.update_password(user, old_password="123", new_password="1234")
    assert right_password is True

    fetched = repo.get_by_login("sava")
    assert fetched.password == "1234"


def test_update_password_with_wrong_old_password_does_not_change_it(db_session):
    repo = UserRepository(db_session)
    user = User(id=None, name="Сава", login="sava", password="123")
    repo.add(user)

    wrong_password = repo.update_password(user, old_password="12", new_password="1234")
    assert wrong_password is False

    fetched = repo.get_by_login("sava")
    assert fetched.password == "123"


def test_add_and_get_review(db_session, a_user, a_sanatorium):
    repo = ReviewRepository(db_session)
    review = Review(
        user_id=a_user.id,
        sanatorium_id=a_sanatorium.id,
        text="test_review",
        rating=4.8,
        created_at="12.04.25",
    )
    repo.add(review)

    fetched = repo.get_by_sanatorium_id(a_sanatorium.id)

    assert fetched is not None
    assert fetched[0].user_id == a_user.id
    assert fetched[0].rating == 4.8


def test_create_and_get_profile(db_session, a_user, some_tags):
    repo = UserRepository(db_session)
    tags = [some_tags[0].id, some_tags[1].id]
    profile = UserProfile(
        id=None,
        user_id=a_user.id,
        goal="лечение",
        budget=5000,
        region="Крым",
        tags=tags,
        budget_weight=1,
        region_weight=1,
        medical_weight=1,
        services_weight=1,
        conditions_weight=1,
    )
    repo.create_profile(profile, tags)

    fetched = repo.get_by_user_id(a_user.id)
    fetched_tag_ids = {t.id for t in fetched.tags}

    assert fetched is not None
    assert fetched_tag_ids == {some_tags[0].id, some_tags[1].id}
    assert fetched.goal == "лечение"


def test_update_profile(db_session, a_profile, some_tags):
    repo = UserRepository(db_session)
    profile = repo.get_by_user_id(a_profile.user_id)
    tags = [some_tags[0].id, some_tags[1].id]

    assert profile is not None
    assert profile.region == "Крым"

    profile.update_profile(
        goal="лечение",
        budget=5000,
        region="Краснодарский край",
        tags=tags,
        budget_weight=1,
        region_weight=1,
        medical_weight=1,
        services_weight=1,
        conditions_weight=1,
    )
    repo.update_profile(profile, tags)

    fetched = repo.get_by_user_id(a_profile.user_id)

    assert fetched is not None
    assert fetched.region == "Краснодарский край"


def test_get_by_tags_finds_sanatorium_with_all_tags(db_session, a_sanatorium, some_tags):
    tags = [t.id for t in some_tags]
    repo = SanatoriumRepository(db_session)

    fetched = repo.get_by_tags(tags)

    assert fetched is not None
    assert fetched[0].tags[0].name == some_tags[0].name


def test_get_by_tags_excludes_sanatorium_missing_a_tag(db_session, a_sanatorium, some_tags):
    tags = [t.id for t in some_tags]
    tags.append(5)
    repo = SanatoriumRepository(db_session)

    fetched = repo.get_by_tags(tags)

    assert len(fetched) == 0


def test_get_by_tags_with_empty_list_returns_all(db_session, a_sanatorium):
    repo = SanatoriumRepository(db_session)

    fetched = repo.get_by_tags([])

    assert fetched is not None
    assert len(fetched) == 1
