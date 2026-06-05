from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from adapters.database import SessionLocal
from adapters.logger import configure_logging, get_logger
from adapters.repository import (
    ReviewRepository,
    SanatoriumRepository,
    TagRepository,
    UserRepository,
)
from domain.exception import (
    DomainError,
    InvalidRequestError,
    ProfileNotFoundError,
    SanatoriumNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
    WrongPasswordError,
)
from domain.goal_programming import recommend
from service_layer.services import (
    add_review,
    change_user_password,
    create_profile,
    login_in,
    update_profile,
    user_created,
)

configure_logging()
log = get_logger(__name__)
app = Flask(__name__)
CORS(app)

EXCEPTION_STATUS_CODES: dict[type[DomainError], int] = {
    UserNotFoundError: 404,
    ProfileNotFoundError: 404,
    SanatoriumNotFoundError: 404,
    WrongPasswordError: 401,
    UserAlreadyExistsError: 409,
    InvalidRequestError: 400,
}


@app.errorhandler(DomainError)
def handle_domain_error(error: DomainError):
    status_code = EXCEPTION_STATUS_CODES.get(type(error), 400)
    error_type = type(error).__name__

    log.warning(
        "domain_error",
        error_type=error_type,
        error_message=str(error),
        status_code=status_code,
    )

    return jsonify(
        {
            "error": error_type,
            "message": str(error),
        }
    ), status_code


@app.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    log.error(
        "unexpected_error",
        error_type=type(error).__name__,
        error_message=str(error),
        exc_info=True,
    )
    return jsonify(
        {
            "error": "InternalServerError",
            "message": "Внутренняя ошибка сервера",
        }
    ), 500


@app.route("/api/tags", methods=["GET"])
def get_tags():
    with SessionLocal() as session:
        tags_repo = TagRepository(session)
        tags = tags_repo.get_all()

        response = []

        for s in tags:
            response.append({"id": s.id, "name": s.name, "category": s.category})
        return jsonify(response)


@app.route("/api/sanatoriums/", methods=["GET"])
def get_sanatoriums():
    with SessionLocal() as session:
        sanat_repo = SanatoriumRepository(session)
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
    with SessionLocal() as session:
        sanat_repo = SanatoriumRepository(session)
        sanat = sanat_repo.get_by_id(id)
        if not sanat:
            raise SanatoriumNotFoundError("Sanatorium not found")
        return jsonify(
            {
                "id": sanat.id,
                "name": sanat.name,
                "budget": sanat.budget,
                "region": sanat.region,
                "tags": [{"id": t.id, "name": t.name, "category": t.category} for t in sanat.tags],
                "food": sanat.food,
                "rating": sanat.rating,
            }
        )


@app.route("/api/reviews/<int:sanatorium_id>", methods=["GET"])
def get_reviews(sanatorium_id):
    with SessionLocal() as session:
        review = ReviewRepository(session).get_by_sanatorium_id(sanatorium_id)
        response = []

        for s in review:
            user = UserRepository(session).get_by_id(s.user_id)
            response.append(
                {
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
    with SessionLocal() as session:
        data = request.get_json()

        add_review(
            user_id=data["user_id"],
            sanatorium_id=data["sanatorium_id"],
            text=data["text"],
            rating=data["rating"],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            session=session,
        )
        return jsonify({"message": "Отзыв отправлен"}), 201


@app.route("/api/register", methods=["POST"])
def register():
    with SessionLocal() as session:
        data = request.get_json()

        user_created(
            name=data["name"], login=data["login"], password=data["password"], session=session
        )
        return jsonify({"message": "Пользователь создан"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    with SessionLocal() as session:
        data = request.get_json()

        user = login_in(data["login"], data["password"], session)
        return jsonify({"id": user.id, "name": user.name, "login": user.login})


@app.route("/api/recommend", methods=["POST"])
def get_recommend():
    with SessionLocal() as session:
        data = request.get_json()
        user_id = data["user_id"]

        profile = UserRepository(session).get_by_user_id(user_id)
        sanatoriums = SanatoriumRepository(session).get_all()

        if not profile:
            raise ProfileNotFoundError("Profile not found")

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
    with SessionLocal() as session:
        data = request.get_json()
        user = UserRepository(session).get_by_id(data["user_id"])

        change_user_password(user, data["old_password"], data["new_password"], session)
        return jsonify({"message": "Пароль изменён"})


@app.route("/api/profile", methods=["PUT", "POST"])
def update_profile_route():
    with SessionLocal() as session:
        data = request.get_json()
        existing_user = UserRepository(session).get_by_user_id(data["user_id"])
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
                session=session,
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
                session=session,
            )
            return jsonify({"message": "Профиль создан"})


if __name__ == "__main__":
    from adapters.database import Base, engine

    Base.metadata.create_all(engine)
    app.run(host="0.0.0.0", port=8000, debug=True)
