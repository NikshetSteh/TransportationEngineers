import datetime
from dataclasses import dataclass

from pydantic import BaseModel

from hardware.low.port import Port


class Robot:
    def __init__(self, port: Port):
        self.port = port
        self.handlers = {}
        self.modules = []

    async def loop(
            self,
            fsm: object
    ):
        async with self.port:
            while True:
                data: bytes | str = await self.port.read()
                print("Got data:", data)

                try:
                    data = data.decode("utf-8")
                except UnicodeDecodeError:
                    print("Can`t read data")
                    continue

                data = data.replace("\n", "").replace("\r", "")

                header = data.split(" ")[0]
                body = data[len(header) + 1:]
                handled = False
                for module in self.modules:
                    if module.check_header(header):
                        await module.handle(data, body)
                        handled = True

                if not handled:
                    print("Error, unknown header:", header)

    def add_module(self, module):
        self.modules.append(module)

    def remove_module(self, module):
        self.modules.remove(module)

    # TODO: Make all functions below

    def check_current_position(self):
        pass

    def move(self, point):
        pass


class RobotModule:
    def check_header(self, header: str) -> bool:
        return False

    async def handle(self, header: str, body: str):
        pass


@dataclass
class RobotPositionInWagon:
    train_number: int
    train_date: datetime.datetime
    wagon_id: int
    point_id: str
    basically_direction: bool


class WagonMapPointData(BaseModel):
    wagon_id: int
    point_id: str
    tags: list[str]


class WagonMapData(BaseModel):
    points: list[WagonMapPointData]
    connections: list[tuple[str, str]]


class WagonMapPoint(RobotModule):
    def __init__(
            self,
            wagon_id: int,
            point_id: str
    ):
        self.wagon_id = wagon_id
        self.point_id = point_id
        self.tags = []


class WagonMap:
    def __init__(self):
        self.points = {}
        self.connections = {}


class MovingModule(RobotModule):
    def __init__(
            self,
            train_number: int,
            train_date: datetime.datetime,
            wagon_id: int,
            point_id: str,
            basically_direction: bool
    ):
        self.current_position = RobotPositionInWagon(
            train_number,
            train_date,
            wagon_id,
            point_id,
            basically_direction
        )

    async def load_map(self):
        pass
