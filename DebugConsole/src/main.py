from users import *
from tickets import *
from cities import *
from engineers import *

while True:
    print(
        "1. Пользователи",
        "2. Билеты",
        "3. Информация о городах",
        "4. Магазины",
        "5. Инженеры",
        sep="\n"
    )
    mode = int(input("Введите номер режима: "))


    def users():
        print(
            "1. Добавить пользователя",
            "2. Просмотреть пользователей",
            "3. Узнать id пользователя",
            "4. Удалить пользователя",
            sep="\n"
        )

        user_mode = int(input("> "))
        match user_mode:
            case 1:
                create_user()
            case 2:
                get_users()
            case 3:
                pass
            case 4:
                delete_user()


    def tickets():
        print(
            "1. Добавить билет",
            "2. Просмотреть билеты",
            "3. Удалить билет",
            sep="\n"
        )

        mode_t = int(input("> "))
        match mode_t:
            case 1:
                create_ticket()
            case 2:
                get_tickets()
            case 3:
                delete_ticket()


    def cities():
        print(
            "1. Добавить достопримечательность",
            "2. Добавить отель",
            "3. Показать достопримечательности",
            "4. Показать отели",
            "5. Удалить достопримечательность",
            "6. Удалить отель",
            sep="\n"
        )
        mode_c = int(input("> "))
        match mode_c:
            case 1:
                create_attraction()
            case 2:
                create_hotel()
            case 3:
                get_attractions()
            case 4:
                get_hotels()
            case 5:
                delete_attraction()
            case 6:
                delete_hotel()


    def store():
        print(
            "1. Создать магазин",
            "2. Редактировать магазин",
            "3. Удалить магазин",
            sep="\n"
        )
        mode_s = int(input("> "))
        match mode_s:
            case 1:
                pass
            case 2:
                items()
            case 3:
                pass


    def items():
        print(
            "1. Добавить товар",
            "2. Редактировать товар",
            "3. Удалить товар",
            sep="\n"
        )

        mode_i = int(input("> "))
        match mode_i:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass


    def engineers():
        print(
            "1. Добавить инженера",
            "2. Показать инженеров",
            "3. Настройка прав",
            "4. Удалить инженера",
            "5. Редактировать карту доступа",
            sep="\n"
        )
        mode_e = int(input("> "))
        match mode_e:
            case 1:
                create_engineer()
            case 2:
                get_engineers()
            case 3:
                set_engineer_privileges()
            case 4:
                delete_engineer()
            case 5:
                set_engineer_cart_id()


    match mode:
        case 1:
            users()
        case 2:
            tickets()
        case 3:
            cities()
        case 4:
            store()
        case 5:
            engineers()
        case _:
            print("Такого режима нет")
