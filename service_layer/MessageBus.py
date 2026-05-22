from domain.model import (
    PasswordChanged,
    PasswordNotChanged,
    ProfileCreated,
    ProfileUpdated,
    RecommendationCalculated,
    ReviewCreated,
    UserLogin,
    UserRegistered,
)
from service_layer.handlers import (
    handle_password_changed,
    handle_password_not_changed,
    handle_profile_created,
    handle_profile_updated,
    handle_recomendations_calculated,
    handle_review_created,
    handle_user_created,
    handle_user_login,
)


class EventsBus:
    def handle(self, event):
        if isinstance(event, PasswordChanged):
            handle_password_changed(event)
        elif isinstance(event, PasswordNotChanged):
            handle_password_not_changed(event)
        elif isinstance(event, UserRegistered):
            handle_user_created(event)
        elif isinstance(event, ProfileCreated):
            handle_profile_created(event)
        elif isinstance(event, ProfileUpdated):
            handle_profile_updated(event)
        elif isinstance(event, UserLogin):
            handle_user_login(event)
        elif isinstance(event, RecommendationCalculated):
            handle_recomendations_calculated(event)
        elif isinstance(event, ReviewCreated):
            handle_review_created(event)
