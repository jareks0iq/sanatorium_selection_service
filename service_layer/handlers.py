def handle_password_changed(event):
    print(f"Пароль пользователя {event.login} изменён")


def handle_password_not_changed(event):
    print(f"Пароль пользователя {event.login} не изменён")


def handle_user_created(event):
    print("Профиль успешно создан")


def handle_profile_created(event):
    print("Профиль создан")


def handle_profile_updated(event):
    print("Профиль обновлён")


def handle_recomendations_calculated(event):
    print(f"Рекомендации для пользователя {event.name} рассчитаны")


def handle_user_login(event):
    print("Вход в аккаунт")


def handle_review_created(event):
    print("Отзыв отправлен")
