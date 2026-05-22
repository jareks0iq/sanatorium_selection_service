from adapters.repository import ReviewRepository, UserRepository
from domain.model import Review, User, UserProfile
from service_layer.MessageBus import EventsBus

event_bus = EventsBus()


def change_user_password(user, old_password: str, new_password: str):
    flag = UserRepository().update_password(user, old_password, new_password)

    user.change_password(flag)

    for event in user.events:
        event_bus.handle(event)

    user.events.clear()

    return flag


def user_created(name: str, login: str, password: str):

    user_repository = UserRepository()
    existing_user = user_repository.get_by_login(login)

    if existing_user:
        raise ValueError(f"Логин {login} уже занят")

    user = User(id=None, name=name, login=login, password=password)

    profile_repository = UserRepository()
    profile_repository.add(user)

    user.register()

    for event in user.events:
        event_bus.handle(event)

    user.events.clear()


def login_in(login: str, password: str):
    user_repository = UserRepository()
    existing_user = user_repository.get_by_login(login)

    if existing_user:
        if password == existing_user.password:
            existing_user.user_log_in()

            for event in existing_user.events:
                event_bus.handle(event)

            existing_user.events.clear()
            return 1
        else:
            return 0
    else:
        return -1


def add_review(user_id: int, sanatorium_id: int, text: str, rating: float, created_at: str):
    review = Review(
        id=None,
        user_id=user_id,
        sanatorium_id=sanatorium_id,
        text=text,
        rating=rating,
        created_at=created_at,
    )
    ReviewRepository().add(review)

    review.created()

    for event in review.events:
        event_bus.handle(event)

    review.events.clear()


def create_profile(
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
):
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

    profile_repository = UserRepository()
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
):

    profile_repository = UserRepository()
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
