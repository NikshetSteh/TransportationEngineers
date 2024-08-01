import requests
import base64
import json

base_url = "http://localhost:8080/base_api/v1"

print("1. Пользователи\n"
    "2. Билеты\n"
    "3. Информация о городах\n"
    "4. Магазины\n"
    "5. Инженеры")

mode = int(input("Введите номер режима: "))

def users():
    print(
        "1. Добавить пользователя\n"
        "2. Просмотреть пользователей\n"
        "3. Узнать id пользователя\n"
        "4. Удалить пользователя"
    )
    mode_u = int(input())
    match mode_u:
        case 1:
            name = input("Введите ФИО: ")
            face = input("Путь к фото: ")

            with open(face, "rb") as file:
                face = file.read()
                face = base64.b64encode(face)

            res = requests.post(base_url + "/admin/user", json={"name":name, "face":face})
            
        case 2:
            res = requests.get(base_url + "/admin/users")

            res:dict = res.json()
            res.pop('page')
            res.pop('size')
            res.pop('pages')
            print(json.dumps(res, indent=4, ensure_ascii=False))
        case 3:
            pass
        case 4:
            id = input("Введите ID: ")
            res = requests.delete(base_url + f"/admin/user/{id}")
            print(res.json())

def tickets():
    print(
        "1. Добавить билет\n"
        "2. Просмотреть билеты\n"
        "3. Удалить билет"
    )
    mode_t = int(input())
    match mode_t:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass

def cityes():
    print(
        "1. Добавить достопримечательность\n"
        "2. Добавить отель\n"
        "3. Удалить достопримечательность\n"
        "4. Удалить отель"
    )
    mode_c = int(input())
    match mode_c:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass

def shop():
    print(
        "1. Создать магазин\n"
        "2. Редактировать магазин\n"
        "3. Удалить магазин\n"
    )
    mode_s = int(input())
    match mode_s:
        case 1:
            pass
        case 2:
            items()
        case 3:
            pass

def items():
    print(
        "1. Добавить товар\n"
        "2. Редактировать товар\n"
        "3. Удалить товар"
    )
    mode_i = int(input())
    match mode_i:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass

def engineers():
    print(
        "1. Добавить инженера\n"
        "2. Редактировать инженера\n"
        "3. Удалить инженера\n"
    )
    mode_e = int(input())
    match mode_e:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass

match mode:
    case 1:
        users()
    case 2:
        tickets()
    case 3:
        cityes()
    case 4:
        shop()
    case 5:
        engineers()

