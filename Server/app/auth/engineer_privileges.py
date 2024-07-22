from enum import Enum


class EngineerPrivileges(Enum):
    ROBOT_LOGIN = "ROBOT_LOGIN"
    STORE_LOGIN = "STORE_LOGIN"


engineer_privileges_translations = {
    EngineerPrivileges.ROBOT_LOGIN: 1,
    EngineerPrivileges.STORE_LOGIN: 2,
}
