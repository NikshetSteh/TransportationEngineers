import datetime
import enum
from dataclasses import dataclass

from pydantic import BaseModel


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


class WagonMapPoint:
    def __init__(
            self,
            wagon_id: int,
            point_id: str,
            tags: list[str] = None
    ):
        self.wagon_id = wagon_id
        self.point_id = point_id
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
        self.checked = False


class DirectionType(enum.Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


class WagonMap:
    def __init__(
            self,
            points: dict[str, WagonMapPoint],
            connections: dict[str, [(str, DirectionType)]]
    ):
        self.points: dict[str, WagonMapPoint] = points
        self.connections: dict[str, [(str, DirectionType)]] = connections

    def get_target_point(self, tag: str) -> WagonMapPoint | None:
        result = None
        for point in self.points.values():
            if tag in point.tags:
                result = point
                break
        return result

    def get_path_to(self, start_point: str, end_point: str) -> list[str] | None:
        stack = [(start_point, [])]
        buffer_graph = self.points.copy()

        while len(stack) > 0:
            buffer_current = stack.pop()
            connections = [i for i in self.connections[buffer_current[0]] if not buffer_graph[i[0]].checked]
            connections_dict = {point_id: direction_type for point_id, direction_type in connections}

            if end_point in connections_dict:
                return buffer_current[1] + [connections_dict[end_point]]

            for point_id, direction_type in connections:
                buffer_graph[point_id].checked = True
                stack.append((point_id, buffer_current[1] + [direction_type]))

        return None


wagon_map = WagonMap(
    points={
        "welcome": WagonMapPoint(0, "welcome", tags=["welcome"]),
        "welcome_out": WagonMapPoint(0, "welcome_out"),
        "welcome_in": WagonMapPoint(0, "welcome_in"),
        "stockroom": WagonMapPoint(0, "stockroom", tags=["stockroom"]),
        "work_1": WagonMapPoint(0, "work_1", tags=["work"]),
        "work_2": WagonMapPoint(0, "work_2", tags=["work"]),
        "work_3": WagonMapPoint(0, "work_3", tags=["work"]),
    },
    connections={
        "welcome": [
            ("welcome_out", DirectionType.LEFT)
        ],
        "welcome_out": [
            ("welcome_in", DirectionType.FORWARD),
            ("welcome", DirectionType.RIGHT)
        ],
        "welcome_in": [
            ("stockroom", DirectionType.FORWARD),
            ("work_1", DirectionType.RIGHT),
            ("welcome_out", DirectionType.BACKWARD)
        ],
        "stockroom": [
            ("welcome_in", DirectionType.BACKWARD)
        ],
        "work_1": [
            ("work_2", DirectionType.RIGHT),
            ("welcome_in", DirectionType.LEFT)
        ],
        "work_2": [
            ("work_3", DirectionType.RIGHT),
            ("work_1", DirectionType.LEFT)
        ],
        "work_3": [
            ("work_2", DirectionType.LEFT)
        ]
    }
)

# print(wagon_map.get_target_point("work"))
# print(
#     wagon_map.get_path_to(
#         start_point="welcome",
#         end_point="work_3"
#     )
# )
# print(
#     wagon_map.get_path_to(
#         start_point="work_3",
#         end_point="welcome"
#     )
# )
