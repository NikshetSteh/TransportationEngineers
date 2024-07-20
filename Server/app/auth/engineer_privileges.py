from enum import Enum


class EngineerPrivileges(Enum):
    ROBOT_LOGIN = "ROBOT_LOGIN"


engineer_privileges_translations = {
    EngineerPrivileges.ROBOT_LOGIN: 1
}
