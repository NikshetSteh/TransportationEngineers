from json import JSONDecodeError, dumps

from requests import Response


def default_print_response(response: Response) -> None:
    print(response.status_code)
    try:
        buffer = response.json()

        print(dumps(buffer, indent=2))
    except JSONDecodeError:
        print(response.text)


def default_print_pagination(response: Response) -> None:
    print(response.status_code)
    try:
        buffer: dict = response.json()

        buffer.pop("page")
        buffer.pop("size")
        buffer.pop("pages")

        print(dumps(buffer, indent=2))
    except JSONDecodeError:
        print(response.text)
