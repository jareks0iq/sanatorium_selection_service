def test_register_creates_user(client):
    response = client.post(
        "/api/register",
        json={"name": "Иван", "login": "ivan", "password": "secret"},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Пользователь создан"


def test_login_with_correct_data(client):
    client.post("api/register", json={"name": "Сава", "login": "sava", "password": "123"})

    response = client.post("api/login", json={"login": "sava", "password": "123"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["login"] == "sava"
    assert data["name"] == "Сава"
    assert "id" in data


def test_login_with_wrong_password_returns_401(client):
    client.post("api/register", json={"name": "Сава", "login": "sava", "password": "123"})

    response = client.post("api/login", json={"login": "sava", "password": "1234"})

    assert response.status_code == 401
    assert "error" in response.get_json()


def test_login_with_unknown_user_returns_404(client):
    response = client.post("api/login", json={"login": "sava", "password": "1234"})

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_get_sanat_returns_sanat(client, a_sanatorium):
    response = client.get("api/sanatoriums/")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1

    sanatorium = data[0]

    assert sanatorium["name"] == "Тестовый санаторий"
    assert "tags" in sanatorium
    assert len(sanatorium["tags"]) > 0


def test_get_active_sanat_by_id_returns_data(client, a_sanatorium):
    response = client.get(f"api/sanatoriums/{a_sanatorium.id}")

    assert response.status_code == 200
    sanatorium = response.get_json()[0]

    assert sanatorium["name"] == "Тестовый санаторий"
    assert "tags" in sanatorium
    assert len(sanatorium["tags"]) > 0


def test_get_non_existent_sanat_by_id_returns_404(client):
    response = client.get("api/sanatoriums/99999")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_create_profile_returns_200(client, a_user, some_tags):
    tags = [some_tags[0].id, some_tags[1].id]
    response = client.post(
        "api/profile",
        json={
            "user_id": a_user.id,
            "goal": "лечение",
            "budget": 5000,
            "region": "Крым",
            "tag_ids": tags,
            "budget_weight": 1,
            "region_weight": 1,
            "medical_weight": 1,
            "services_weight": 1,
            "conditions_weight": 1,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Профиль создан"


def test_update_profile_via_api(client, a_profile, some_tags):
    tags = [some_tags[0].id, some_tags[1].id]
    response = client.put(
        "api/profile",
        json={
            "user_id": a_profile.user_id,
            "goal": "лечение",
            "budget": 8000,
            "region": "Краснодарский край",
            "tag_ids": tags,
            "budget_weight": 1,
            "region_weight": 1,
            "medical_weight": 1,
            "services_weight": 1,
            "conditions_weight": 1,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Профиль обновлён"


def test_get_recommend_via_api(client, a_profile, some_tags, a_sanatorium):
    response = client.post("api/recommend", json={"user_id": a_profile.user_id})

    assert response.status_code == 200
    assert len(response.get_json()) == 1
