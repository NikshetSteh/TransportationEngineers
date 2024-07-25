from enum import Enum


class EngineerPrivileges(Enum):
    ROBOT_LOGIN = "ROBOT_LOGIN"
    STORE_LOGIN = "STORE_LOGIN"
    ROBOT_ADMIN = "ROBOT_ADMIN"


engineer_privileges_translations = {
    EngineerPrivileges.ROBOT_LOGIN: 1,
    EngineerPrivileges.STORE_LOGIN: 2,
    EngineerPrivileges.ROBOT_ADMIN: 4,
}
