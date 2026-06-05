from adapters.logger import get_logger

log = get_logger(__name__)


def handle_password_changed(event):
    log.info("user_changed_password", user_id=event.user_id)


def handle_password_not_changed(event):
    log.warning("user_password_not_changed", user_id=event.user_id)


def handle_user_created(event):
    log.info("user_registered", user_id=event.user_id)


def handle_profile_created(event):
    log.info("profile_created", user_id=event.user_id, user_profile_id=event.profile_id)


def handle_profile_updated(event):
    log.info("profile_updated", user_id=event.user_id, user_profile_id=event.profile_id)


def handle_recomendations_calculated(event):
    log.info("get_recommendations", user_id=event.user_id)


def handle_user_login(event):
    log.info("user_log_in", user_id=event.user_id)


def handle_review_created(event):
    log.info(
        "review_created",
        review_id=event.review_id,
        sanatorium_id=event.sanatorium_id,
        user_id=event.user_id,
    )
