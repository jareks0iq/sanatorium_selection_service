from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from adapters.repository import (
    ReviewRepository,
    SanatoriumRepository,
    TagRepository,
    UserRepository,
)
from domain.goal_programming import recommend
from service_layer.services import (
    add_review,
    change_user_password,
    create_profile,
    update_profile,
    user_created,
)

app = Flask(__name__)
CORS(app)


@app.route("/api/tags", methods=["GET"])
def get_tags():
    tags_repo = TagRepository()
    tags = tags_repo.get_all()

    response = []

    for s in tags:
        response.append({"id": s.id, "name": s.name, "category": s.category})
    return jsonify(response)


@app.route("/api/sanatoriums/", methods=["GET"])
def get_sanatoriums():
    sanat_repo = SanatoriumRepository()
    sanat = sanat_repo.get_all()

    response = []

    for s in sanat:
        response.append(
            {
                "id": s.id,
                "name": s.name,
                "budget": s.budget,
                "region": s.region,
                "tags": [{"id": t.id, "name": t.name, "category": t.category} for t in s.tags],
                "food": s.food,
                "rating": s.rating,
            }
        )
    return jsonify(response)


@app.route("/api/sanatoriums/<int:id>", methods=["GET"])
def get_sanatorium_by_id(id: int):
    sanat_repo = SanatoriumRepository()
    sanat = sanat_repo.get_by_id(id)

    if sanat:
        response = [
            {
                "id": sanat.id,
                "name": sanat.name,
                "budget": sanat.budget,
                "region": sanat.region,
                "tags": [{"id": t.id, "name": t.name, "category": t.category} for t in sanat.tags],
                "food": sanat.food,
                "rating": sanat.rating,
            }
        ]
        return jsonify(response)
    else:
        return jsonify({"error": "Санаторий не найден"}), 404


@app.route("/api/reviews/<int:sanatorium_id>", methods=["GET"])
def get_reviews(sanatorium_id):
    review = ReviewRepository().get_by_sanatorium_id(sanatorium_id)
    response = []

    for s in review:
        user = UserRepository().get_by_id(s.user_id)
        response.append(
            {
                "id": s.id,
                "user_id": s.user_id,
                "user_name": user.name,
                "sanatorium_id": s.sanatorium_id,
                "text": s.text,
                "rating": s.rating,
                "created_at": s.created_at,
            }
        )
    return jsonify(response)


@app.route("/api/reviews", methods=["POST"])
def route_add_review():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных"}), 400

    add_review(
        user_id=data["user_id"],
        sanatorium_id=data["sanatorium_id"],
        text=data["text"],
        rating=data["rating"],
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    return jsonify({"message": "Отзыв отправлен"}), 201


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных"}), 400
    try:
        user_created(name=data["name"], login=data["login"], password=data["password"])
        return jsonify({"message": "Пользователь создан"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных"}), 400

    user = UserRepository().get_by_login(data["login"])

    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    if user.password != data["password"]:
        return jsonify({"error": "Неверный пароль"}), 401

    return jsonify({"id": user.id, "name": user.name, "login": user.login})


@app.route("/api/recommend", methods=["POST"])
def get_recommend():
    data = request.get_json()
    user_id = data["user_id"]

    profile = UserRepository().get_by_user_id(user_id)
    sanatoriums = SanatoriumRepository().get_all()

    results = recommend(sanatoriums, profile)

    response = []
    for score, s in results:
        response.append(
            {
                "id": s.id,
                "name": s.name,
                "budget": s.budget,
                "region": s.region,
                "score": round(score, 4),
                "tags": [{"id": t.id, "name": t.name, "category": t.category} for t in s.tags],
                "food": s.food,
                "rating": s.rating,
            }
        )
    return jsonify(response)


@app.route("/api/password", methods=["PUT"])
def change_password_route():
    data = request.get_json()
    user = UserRepository().get_by_id(data["user_id"])

    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    flag = change_user_password(user, data["old_password"], data["new_password"])
    if not flag:
        return jsonify({"error": "Неверный пароль"})
    else:
        return jsonify({"message": "Пароль изменён"})


@app.route("/api/profile", methods=["PUT", "POST"])
def update_profile_route():
    data = request.get_json()
    existing_user = UserRepository().get_by_user_id(data["user_id"])
    if existing_user:
        update_profile(
            id=data["user_id"],
            goal=data["goal"],
            budget=data["budget"],
            region=data["region"],
            tag_ids=data["tag_ids"],
            budget_weight=data["budget_weight"],
            region_weight=data["region_weight"],
            medical_weight=data["medical_weight"],
            services_weight=data["services_weight"],
            conditions_weight=data["conditions_weight"],
        )
        return jsonify({"message": "Профиль обновлён"})
    else:
        create_profile(
            id=data["user_id"],
            goal=data["goal"],
            budget=data["budget"],
            region=data["region"],
            tag_ids=data["tag_ids"],
            budget_weight=data["budget_weight"],
            region_weight=data["region_weight"],
            medical_weight=data["medical_weight"],
            services_weight=data["services_weight"],
            conditions_weight=data["conditions_weight"],
        )
        return jsonify({"message": "Профиль создан"})


if __name__ == "__main__":
    from adapters.database import Base, engine

    Base.metadata.create_all(engine)
    app.run(host="0.0.0.0", port=5000, debug=True)
