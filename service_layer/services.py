from adapters.repository import ReviewRepository, UserRepository
from domain.exception import UserAlreadyExistsError, UserNotFoundError, WrongPasswordError
from domain.model import Review, User, UserProfile
from service_layer.message_bus import EventsBus

event_bus = EventsBus()


def change_user_password(user, old_password: str, new_password: str, session):
    flag = UserRepository(session).update_password(user, old_password, new_password)

    user.change_password(flag)

    for event in user.events:
        event_bus.handle(event)

    user.events.clear()

    if not flag:
        raise WrongPasswordError("Wrong password")
    return flag


def user_created(name: str, login: str, password: str, session):
    user_repository = UserRepository(session)
    existing_user = user_repository.get_by_login(login)

    if existing_user:
        raise UserAlreadyExistsError(f"User with login {login} is already occupied")
    user = User(id=None, name=name, login=login, password=password)

    profile_repository = UserRepository(session)
    profile_repository.add(user)

    user.register()

    for event in user.events:
        event_bus.handle(event)

    user.events.clear()


def login_in(login: str, password: str, session):
    user_repository = UserRepository(session)
    existing_user = user_repository.get_by_login(login)

    if existing_user:
        if password == existing_user.password:
            existing_user.user_log_in()

            for event in existing_user.events:
                event_bus.handle(event)

            existing_user.events.clear()
            return existing_user
        else:
            raise WrongPasswordError("Wrong password")
    else:
        raise UserNotFoundError(f"User with login {login} not found")


def add_review(
    user_id: int, sanatorium_id: int, text: str, rating: float, created_at: str, session
):
    review = Review(
        user_id=user_id,
        sanatorium_id=sanatorium_id,
        text=text,
        rating=rating,
        created_at=created_at,
    )
    ReviewRepository(session).add(review)

    review.created()

    for event in review.events:
        event_bus.handle(event)

    review.events.clear()


def create_profile(
    id: int | None,
    goal: str,
    budget: int,
    region: str,
    tag_ids: list[int],
    budget_weight: int,
    region_weight: int,
    medical_weight: int,
    services_weight: int,
    conditions_weight: int,
    session,
):
    if id is None:
        raise ValueError("Cannot create profile for unsaved user")
    profile = UserProfile(
        id=None,
        user_id=id,
        goal=goal,
        budget=budget,
        region=region,
        tags=tag_ids,
        budget_weight=budget_weight,
        region_weight=region_weight,
        medical_weight=medical_weight,
        services_weight=services_weight,
        conditions_weight=conditions_weight,
    )

    profile_repository = UserRepository(session)
    profile_repository.create_profile(profile, tag_ids)

    profile.created_profile()

    for event in profile.events:
        event_bus.handle(event)

    profile.events.clear()


def update_profile(
    id,
    goal: str,
    budget: int,
    region: str,
    tag_ids: list[int],
    budget_weight: int,
    region_weight: int,
    medical_weight: int,
    services_weight: int,
    conditions_weight: int,
    session,
):

    profile_repository = UserRepository(session)
    profile = profile_repository.get_by_user_id(id)

    profile.update_profile(
        goal,
        budget,
        region,
        tag_ids,
        budget_weight,
        region_weight,
        medical_weight,
        services_weight,
        conditions_weight,
    )

    profile_repository.update_profile(profile, tag_ids)

    for event in profile.events:
        event_bus.handle(event)

    profile.events.clear()
