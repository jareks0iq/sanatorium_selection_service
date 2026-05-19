class User: #login, password
    def __init__(self, id: int, name: str, login: str, password: str):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.events = []

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

class UserProfile: #Предпочтения пользователя, критерии выбора
    def __init__(self, id: int, user_id: int, goal: str, budget: int, region: str, tags: list[int],
                 budget_weight: int, region_weight: int, medical_weight: int, services_weight: int, conditions_weight: int):
        self.id = id
        self.user_id = user_id
        self.goal = goal
        #желаемые критерии
        self.budget = budget
        self.region = region
        self.tags = tags
        #важность критериев
        self.budget_weight = budget_weight
        self.region_weight = region_weight
        self.medical_weight = medical_weight
        self.conditions_weight = conditions_weight
        self.services_weight = services_weight
        self.events = []
    def created_profile(self):
        self.events.append(ProfileCreated(self.user_id))
    def update_profile(self, goal: str, budget: int, region: str, tags: list[int],
                 budget_weight: int, region_weight: int, medical_weight: int, services_weight: int, conditions_weight: int):
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
        self.events.append(ProfileUpdated(self.id))

class Sanatorium: #Общие сведения о санаториуме
    def __init__(self, id: int, name: str, budget: int, region: str, tags: list, food: str, rating: float):
        self.id = id
        self.name = name
        #факторы для пользователя
        self.budget = budget
        self.region = region
        self.tags = tags
        #доп сведения
        self.food = food
        self.rating = rating

class Tag:
    def __init__(self, id: int, name: str, category: str):
        self.id = id
        self.name = name
        self.category = category

class Review:
    def __init__(self, id: int, user_id: int, sanatorium_id: int, text: str, rating: float, created_at: str):
        self.id = id
        self.user_id = user_id
        self.sanatorium_id = sanatorium_id
        self.text = text
        self.rating = rating
        self.created_at = created_at
        self.events = []
    def created(self):
        self.events.append(ReviewCreated(self.id))

class UserLogin:
    def __init__(self, user_id: int):
        self.user_id = user_id

class PasswordChanged:
    def __init__(self, login: str):
        self.login = login

class PasswordNotChanged:
    def __init__(self, login: str):
        self.login = login

class UserRegistered:
    def __init__(self, user_id: int):
        self.user_id = user_id

class ProfileCreated:
    def __init__(self, user_id: int):
        self.user_id = user_id

class ProfileUpdated:
    def __init__(self, user_id: int):
        self.user_id = user_id

class Recomendation_Calculated:
    def __init__(self, user_id, sanatorium_ids: list):
        self.user_id = user_id
        self.sanatorium_ids = sanatorium_ids

class ReviewCreated:
    def __init__(self, id: int):
        self.id = id