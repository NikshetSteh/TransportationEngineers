from users import *
from tickets import *
from cities import *
from engineers import *
from stores import *
from store_items import *
from debug_data import *
from train_stores import *

while True:
    print(
        "1. Пользователи",
        "2. Билеты",
        "3. Информация о городах",
        "4. Магазины",
        "5. Инженеры",
        "6. Загрузка данных для тестирования",
        "7. Магазины поездов",
        sep="\n"
    )
    mode = int(input("Введите номер режима: "))


    def users():
        print(
            "1. Добавить пользователя",
            "2. Просмотреть пользователей",
            "3. Узнать id пользователя",
            "4. Удалить пользователя",
            "5. Привязать keycloak",
            "6. Отвязать keycloak",
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
            case 5:
                link_keycloak()
            case 6:
                unlink_keycloak()


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
            "2. Показать магазины",
            "3. Удалить магазин",
            "4. Показать магазин",
            "5. Редактировать магазин",
            sep="\n"
        )
        mode_s = int(input("> "))
        match mode_s:
            case 1:
                create_store()
            case 2:
                get_stores()
            case 3:
                delete_store()
            case 4:
                get_store()
            case 5:
                items()


    def items():
        print(
            "1. Добавить товар",
            "2. Показать товары",
            "3. Удалить товар",
            "4. Обновить товар",
            "5. Показать задачи",
            "6. Отметить задачу выполненной",
            "7. Загрузить товары",
            sep="\n"
        )

        mode_i = int(input("> "))
        match mode_i:
            case 1:
                create_store_item()
            case 2:
                get_store_items()
            case 3:
                delete_store_item()
            case 4:
                update_store_item()
            case 5:
                get_store_tasks()
            case 6:
                mark_task_as_done()
            case 7:
                load_items()


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


    def trains_stores():
        print(
            "1. Добавить магазин к поезду",
            "2. Показать магазины поезда",
            "3. Удалить привязку магазина к поезду",
            sep="\n"
        )

        mode_t = int(input("> "))
        match mode_t:
            case 1:
                add_train_store()
            case 2:
                get_train_stores()
            case 3:
                delete_train_store()


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
        case 6:
            load_debug_data()
        case 7:
            trains_stores()
        case _:
            print("Такого режима нет")
