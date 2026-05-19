from adapters.database import engine, Base, SessionLocal
from service_layer.services import user_created, create_profile, login_in
from adapters.orm import TagOrm, UserORM
from seed import seed_tags, seed_sanatoriums
from adapters.repository import UserRepository, SanatoriumRepository
from domain.model import User, Sanatorium, Tag
from domain.goal_programming import recommend
import os
Base.metadata.create_all(engine)
session = SessionLocal()

os.system("cls")
while True:
    print("1) Создать аккаунт")
    print("2) Войти в аккаунт")
    print("3) Выход")
    k = int(input())
    if k == 1:
        os.system("cls")
        print("Введите имя:")
        name = input()
        print("Введите логин:")
        login = input()
        print("Введите пароль:")
        password = input()

        user_created(name, login, password)
        os.system("cls")

        print("Введите цель отдыха")
        goal = input()
        print("Введите бюджет за сутки")
        budget = int(input())
        print("Введите регион")
        region = input()

        tags = []
        print("Профили медицины:")
        print("")
        medical_orm = session.query(TagOrm).filter_by(category="medical").all()
        med = [Tag(t.id, t.name, t.category) for t in medical_orm]
        for i in range(0, len(med)):
            print(med[i].id, med[i].name)
        medical = [int(x) for x in input("Введите числа желаемых профилей медицины через запятую: ").split(',')]

        print("Услуги:")
        services_orm = session.query(TagOrm).filter_by(category="services").all()
        serv = [Tag(t.id, t.name, t.category) for t in services_orm]
        for i in range(0, len(serv)):
            print(serv[i].id, serv[i].name)
        services = [int(x) for x in input("Введите числа желаемых услуг через запятую: ").split(',')]

        print("Условия:")
        conditions_orm = session.query(TagOrm).filter_by(category="conditions").all()
        cond = [Tag(t.id, t.name, t.category) for t in conditions_orm]
        for i in range(0, len(cond)):
            print(cond[i].id, cond[i].name)
        conditions = [int(x) for x in input("Введите числа желаемых условий через запятую: ").split(',')]

        tags.extend(medical)
        tags.extend(services)
        tags.extend(conditions)

        print("Введите от 1 до 10 важность бюджета:")
        budget_weight = int(input())

        print("Введите от 1 до 10 важность региона:")
        region_weight = int(input())

        print("Введите от 1 до 10 важность медицинского профиля:")
        medical_weight = int(input())

        print("Введите от 1 до 10 важность услуг:")
        services_weight = int(input())

        print("Введите от 1 до 10 важность условий:")
        conditions_weight = int(input())

        id = session.query(UserORM).filter_by(login=login).first()

        create_profile(id.id, goal, budget, region, tags, budget_weight, region_weight, medical_weight, services_weight, conditions_weight)
        os.system("cls")

        while True:
            print("1) Вывести рекомендованные санатории")
            print("2) Вывести все санатории")
            print("3) Вывести фильтры пользователя")
            key = int(input())
            if key == 1:
                while True:
                    sanat = SanatoriumRepository()
                    profile = UserRepository()
                    print(recommend(sanat.get_all(), profile.get_by_user_id(id)))
                    print("Нажмите любую клавишу для выхода")
                    temp = input()
                    break
            elif key == 2:
                sanat = SanatoriumRepository()

                result = sanat.get_all()

                sanatoriums = []

                for s in range(0, len(result)):
                    temp = []

                    temp.append(result[s].id)
                    temp.append(result[s].name)
                    temp.append(result[s].budget)
                    temp.append(result[s].region)
                    tag_ids = [Tag(id=t.id, name=t.name, category=t.category) for t in result[s].tags]
                    for i in range(0, len(tag_ids)):
                        temp.append(tag_ids[i].id)
                        temp.append(tag_ids[i].name)
                        temp.append(tag_ids[i].category)
                    temp.append(result[s].tags)
                    temp.append(result[s].food)
                    temp.append(result[s].feedback)
                    temp.append(result[s].rating)
                    sanatoriums.append(temp)

                print(sanatoriums)
    elif k == 2:
        os.system("cls")
        print("Введите логин:")
        login = input()
        print("Введите пароль:")
        password = input()
        login_in(login, password)

        user = UserRepository().get_by_login(login)
        profile = UserRepository().get_by_user_id(user.id)

        while True:
            print("1) Вывести рекомендованные санатории")
            print("2) Вывести все санатории")
            print("3) Вывести фильтры пользователя")
            key = int(input())
            if key == 1:
                while True:
                    sanat = SanatoriumRepository()
                    result = recommend(sanat.get_all(), profile)
                    for score, s in result:
                        print(f"{s.name} — score: {round(score, 4)}, цена: {s.budget}, регион: {s.region}")
                    print("Нажмите любую клавишу для выхода")
                    temp = input()
                    break
            elif key == 2:
                sanat = SanatoriumRepository()

                result = sanat.get_all()

                sanatoriums = []

                for s in range(0, len(result)):
                    temp = []

                    temp.append(result[s].id)
                    temp.append(result[s].name)
                    temp.append(result[s].budget)
                    temp.append(result[s].region)
                    tag_ids = [Tag(id=t.id, name=t.name, category=t.category) for t in result[s].tags]
                    for i in range(0, len(tag_ids)):
                        temp.append(tag_ids[i].id)
                        temp.append(tag_ids[i].name)
                        temp.append(tag_ids[i].category)
                    temp.append(result[s].tags)
                    temp.append(result[s].food)
                    temp.append(result[s].feedback)
                    temp.append(result[s].rating)
                    sanatoriums.append(temp)

                print(sanatoriums)