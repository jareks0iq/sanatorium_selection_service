import json

from adapters.database import Base, SessionLocal, engine
from adapters.orm import SanatoriumORM, TagOrm


def seed_tags(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        json_tags = json.load(f)

    session = SessionLocal()
    tags_to_add = []
    for i in range(len(json_tags)):
        for j in range(len(json_tags[i]["name"])):
            tag_orm = TagOrm(name=json_tags[i]["name"][j], category=json_tags[i]["category"])
            tags_to_add.append(tag_orm)
    session.add_all(tags_to_add)
    session.commit()


def seed_sanatoriums(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        json_sanatoriums = json.load(f)

    session = SessionLocal()

    all_tags = session.query(TagOrm).all()
    tag_dict = {tag.name: tag for tag in all_tags}

    for s in json_sanatoriums:
        sanatoriums_tags_list = []
        for tag_name in s["medical"] + s["services"] + s["conditions"]:
            if tag_name in tag_dict:
                sanatoriums_tags_list.append(tag_dict[tag_name])

        sanatorium = SanatoriumORM(
            name=s["name"],
            budget=s["budget"],
            region=s["region"],
            food=s["food"],
            rating=s["rating"],
            tags=sanatoriums_tags_list,
        )
        session.add(sanatorium)
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session = SessionLocal()
    existing_tags = session.query(TagOrm).first()
    session.close()

    if not existing_tags:
        print("БД пустая, выполняю seed...")
        seed_tags("tags.json")
        seed_sanatoriums("sanatoriums.json")
        print("Seed завершён!")
    else:
        print("Данные уже есть, seed пропущен")
