from sqlalchemy import func

from adapters.database import sanatorium_tags
from adapters.orm import ReviewORM, SanatoriumORM, TagOrm, UserORM, UserProfileORM
from domain.model import Review, Sanatorium, Tag, User, UserProfile


class UserRepository:
    def __init__(self, session):
        self.session = session

    def add(self, user):
        user_orm = UserORM(name=user.name, login=user.login, password=user.password)
        self.session.add(user_orm)
        self.session.commit()
        user.id = user_orm.id

    def get_by_login(self, login):  # проверяем занят ли login и для проверки пароля
        active_user = self.session.query(UserORM).filter_by(login=login).first()
        if active_user:
            return User(
                id=active_user.id,
                name=active_user.name,
                login=active_user.login,
                password=active_user.password,
            )
        return None

    def get_by_id(
        self, id
    ):  # когда пользователь залогинен и делает какие-то действия, например, смена пароля
        active_user = self.session.query(UserORM).filter_by(id=id).first()
        if active_user:
            return User(
                id=active_user.id,
                name=active_user.name,
                login=active_user.login,
                password=active_user.password,
            )
        return None

    def create_profile(self, profile, tag_ids: list[int]):
        tags_orm = self.session.query(TagOrm).filter(TagOrm.id.in_(tag_ids)).all()

        user_profile_orm = UserProfileORM(
            user_id=profile.user_id,
            goal=profile.goal,
            budget=profile.budget,
            region=profile.region,
            tags=tags_orm,
            budget_weight=profile.budget_weight,
            region_weight=profile.region_weight,
            medical_weight=profile.medical_weight,
            conditions_weight=profile.conditions_weight,
            services_weight=profile.services_weight,
        )
        self.session.add(user_profile_orm)
        self.session.commit()
        profile.id = user_profile_orm.id

    def get_by_user_id(self, user_id):
        active_profile = self.session.query(UserProfileORM).filter_by(user_id=user_id).first()
        if active_profile:
            return UserProfile(
                id=active_profile.id,
                user_id=active_profile.user_id,
                goal=active_profile.goal,
                budget=active_profile.budget,
                region=active_profile.region,
                tags=active_profile.tags,
                budget_weight=active_profile.budget_weight,
                region_weight=active_profile.region_weight,
                medical_weight=active_profile.medical_weight,
                conditions_weight=active_profile.conditions_weight,
                services_weight=active_profile.services_weight,
            )
        return None

    def update_profile(self, profile, tag_ids: list[int]):
        tag_orm = self.session.query(TagOrm).filter(TagOrm.id.in_(tag_ids)).all()

        profile_orm = self.session.query(UserProfileORM).filter_by(user_id=profile.user_id).first()
        if profile_orm:
            profile_orm.goal = profile.goal
            profile_orm.budget = profile.budget
            profile_orm.region = profile.region
            profile_orm.tags = tag_orm
            profile_orm.budget_weight = profile.budget_weight
            profile_orm.region_weight = profile.region_weight
            profile_orm.medical_weight = profile.medical_weight
            profile_orm.conditions_weight = profile.conditions_weight
            profile_orm.services_weight = profile.services_weight

            self.session.commit()
        return None

    def update_password(self, user, old_password: str, new_password: str):
        user_orm = self.session.query(UserORM).filter_by(id=user.id).first()
        if user_orm.password == old_password:
            user_orm.password = new_password
            self.session.commit()
            return True
        else:
            return False


class SanatoriumRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        sanatorium_orm = self.session.query(SanatoriumORM).all()

        result = []

        for s in sanatorium_orm:
            tag_ids = [Tag(id=t.id, name=t.name, category=t.category) for t in s.tags]
            sanatorium = Sanatorium(
                id=s.id,
                name=s.name,
                budget=s.budget,
                region=s.region,
                tags=tag_ids,
                food=s.food,
                rating=s.rating,
            )
            result.append(sanatorium)
        return result

    def get_by_id(self, id):
        sanatorium_orm = self.session.query(SanatoriumORM).filter_by(id=id).first()

        if sanatorium_orm:
            tag_ids = [Tag(id=t.id, name=t.name, category=t.category) for t in sanatorium_orm.tags]

            return Sanatorium(
                id=sanatorium_orm.id,
                name=sanatorium_orm.name,
                budget=sanatorium_orm.budget,
                region=sanatorium_orm.region,
                tags=tag_ids,
                food=sanatorium_orm.food,
                rating=sanatorium_orm.rating,
            )
        return None

    def get_by_tags(self, tag_ids: list[int]):
        if not tag_ids:
            return self.get_all()
        matching_ids = (
            self.session.query(sanatorium_tags.c.sanatorium_id)
            .filter(sanatorium_tags.c.tag_id.in_(tag_ids))
            .group_by(sanatorium_tags.c.sanatorium_id)
            .having(func.count(sanatorium_tags.c.tag_id) == len(tag_ids))
            .all()
        )

        ids = [row[0] for row in matching_ids]

        if not ids:
            return []

        sanatorium_orm = self.session.query(SanatoriumORM).filter(SanatoriumORM.id.in_(ids)).all()

        result = []

        for s in sanatorium_orm:
            tags = [Tag(id=t.id, name=t.name, category=t.category) for t in s.tags]
            sanatorium = Sanatorium(
                id=s.id,
                name=s.name,
                budget=s.budget,
                region=s.region,
                tags=tags,
                food=s.food,
                rating=s.rating,
            )
            result.append(sanatorium)
        return result


class TagRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        tag_orm = self.session.query(TagOrm).all()

        result = []

        for s in tag_orm:
            tag = Tag(id=s.id, name=s.name, category=s.category)
            result.append(tag)

        return result


class ReviewRepository:
    def __init__(self, session):
        self.session = session

    def add(self, review):
        review_orm = ReviewORM(
            user_id=review.user_id,
            sanatorium_id=review.sanatorium_id,
            text=review.text,
            rating=review.rating,
            created_at=review.created_at,
        )
        self.session.add(review_orm)
        self.session.commit()
        review.id = review_orm.id

    def get_by_sanatorium_id(self, sanatorium_id: int):
        active_review = self.session.query(ReviewORM).filter_by(sanatorium_id=sanatorium_id).all()

        result = []

        for s in active_review:
            review = Review(
                user_id=s.user_id,
                sanatorium_id=s.sanatorium_id,
                text=s.text,
                rating=s.rating,
                created_at=s.created_at,
            )
            result.append(review)
        return result
