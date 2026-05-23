class Tag:
    def __init__(self, id: int | None, name: str, category: str):
        self.id = id
        self.name = name
        self.category = category


class User:  # login, password
    def __init__(self, id: int | None, name: str, login: str, password: str):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.events: list[Event] = []

    def register(self):
        self.events.append(UserRegistered(self.id))

    def change_password(self, changed_password):
        if changed_password:
            self.events.append(PasswordChanged(self.login))
            return True
        else:
            self.events.append(PasswordNotChanged(self.login))
            return False

    def user_log_in(self):
        self.events.append(UserLogin(self.id))


class UserProfile:  # Предпочтения пользователя, критерии выбора
    def __init__(
        self,
        id: int | None,
        user_id: int,
        goal: str,
        budget: int,
        region: str,
        tags: list[int],
        budget_weight: int,
        region_weight: int,
        medical_weight: int,
        services_weight: int,
        conditions_weight: int,
    ):
        self.id = id
        self.user_id = user_id
        self.goal = goal
        # желаемые критерии
        self.budget = budget
        self.region = region
        self.tags = tags
        # важность критериев
        self.budget_weight = budget_weight
        self.region_weight = region_weight
        self.medical_weight = medical_weight
        self.conditions_weight = conditions_weight
        self.services_weight = services_weight
        self.events: list[Event] = []

    def created_profile(self):
        self.events.append(ProfileCreated(self.user_id))

    def update_profile(
        self,
        goal: str,
        budget: int,
        region: str,
        tags: list[int],
        budget_weight: int,
        region_weight: int,
        medical_weight: int,
        services_weight: int,
        conditions_weight: int,
    ):
        self.goal = goal
        # желаемые критерии
        self.budget = budget
        self.region = region
        self.tags = tags
        # важность критериев
        self.budget_weight = budget_weight
        self.region_weight = region_weight
        self.medical_weight = medical_weight
        self.services_weight = services_weight
        self.conditions_weight = conditions_weight
        assert self.id is not None
        self.events.append(ProfileUpdated(self.id))


class Sanatorium:  # Общие сведения о санаториуме
    def __init__(
        self,
        id: int | None,
        name: str,
        budget: int,
        region: str,
        tags: list[Tag],
        food: str,
        rating: float,
    ):
        self.id = id
        self.name = name
        # факторы для пользователя
        self.budget = budget
        self.region = region
        self.tags = tags
        # доп сведения
        self.food = food
        self.rating = rating


class Review:
    def __init__(self, user_id: int, sanatorium_id: int, text: str, rating: float, created_at: str):
        self.user_id = user_id
        self.sanatorium_id = sanatorium_id
        self.text = text
        self.rating = rating
        self.created_at = created_at
        self.events: list[Event] = []

    def created(self):
        self.events.append(ReviewCreated(self.sanatorium_id))


class Event:
    pass


class UserLogin(Event):
    def __init__(self, user_id: int):
        self.user_id = user_id


class PasswordChanged(Event):
    def __init__(self, login: str):
        self.login = login


class PasswordNotChanged(Event):
    def __init__(self, login: str):
        self.login = login


class UserRegistered(Event):
    def __init__(self, user_id: int):
        self.user_id = user_id


class ProfileCreated(Event):
    def __init__(self, user_id: int):
        self.user_id = user_id


class ProfileUpdated(Event):
    def __init__(self, user_id: int):
        self.user_id = user_id


class RecommendationCalculated(Event):
    def __init__(self, user_id, sanatorium_ids: list):
        self.user_id = user_id
        self.sanatorium_ids = sanatorium_ids


class ReviewCreated(Event):
    def __init__(self, sanatorium_id: int):
        self.sanatorium_id = sanatorium_id
