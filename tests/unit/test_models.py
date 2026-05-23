from domain.model import (
    PasswordChanged,
    PasswordNotChanged,
    ProfileCreated,
    ProfileUpdated,
    Review,
    ReviewCreated,
    User,
    UserLogin,
    UserProfile,
    UserRegistered,
)


def make_user(name="Saveliy", login="jareks", password="123"):
    return User(id=1, name=name, login=login, password=password)


def make_profile(
    budget=50000,
    region="Краснодарский край",
    tags=None,
    budget_weight=0,
    region_weight=0,
    medical_weight=0,
    services_weight=0,
    conditions_weight=0,
):
    return UserProfile(
        id=1,
        user_id=1,
        goal="лечение",
        budget=budget,
        region=region,
        tags=tags if tags is not None else [],
        budget_weight=budget_weight,
        region_weight=region_weight,
        medical_weight=medical_weight,
        services_weight=services_weight,
        conditions_weight=conditions_weight,
    )


def make_review(text="Test Review", rating=5.0):
    return Review(user_id=1, sanatorium_id=1, text=text, rating=rating, created_at="22.05.2026")


def test_register_adds_user_registered_event():
    user = make_user()

    user.register()

    assert len(user.events) == 1
    assert isinstance(user.events[0], UserRegistered)


def test_login_adds_user_login_event():
    user = make_user()

    user.user_log_in()

    assert len(user.events) == 1
    assert isinstance(user.events[0], UserLogin)


def test_right_password_changed_adds_password_changed_event():
    user = make_user()

    result = user.change_password(True)

    assert result is True
    assert len(user.events) == 1
    assert isinstance(user.events[0], PasswordChanged)


def test_wrong_password_changed_adds_password_not_changed_event():
    user = make_user()

    result = user.change_password(False)

    assert result is False
    assert len(user.events) == 1
    assert isinstance(user.events[0], PasswordNotChanged)


def test_created_profile_adds_created_profile_event():
    profile = make_profile()

    profile.created_profile()

    assert len(profile.events) == 1
    assert isinstance(profile.events[0], ProfileCreated)


def test_updated_profile_adds_profile_updated_event():
    profile = make_profile()

    profile.update_profile(
        goal="лечение",
        budget=5000,
        region="Крым",
        tags=[],
        budget_weight=0,
        region_weight=0,
        medical_weight=0,
        services_weight=0,
        conditions_weight=0,
    )

    assert len(profile.events) == 1
    assert isinstance(profile.events[0], ProfileUpdated)


def test_new_review_adds_review_created_event():
    review = make_review()

    review.created()

    assert len(review.events) == 1
    assert isinstance(review.events[0], ReviewCreated)
