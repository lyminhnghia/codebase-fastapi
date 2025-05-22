from enum import Enum


class ErrorCode(str, Enum):
    NOT_FOUND_SUCH_ITEM = "40433000"
    NO_PERMISSION = "40333000"

    UNAUTHORIZED = "40133000"
    UNAUTHENTICATED = "40133001"

    INTERNAL_SERVER_ERROR = "50033000"


ERROR_MESSAGES = {
    ErrorCode.NOT_FOUND_SUCH_ITEM.value: "Not found such item",
    ErrorCode.NO_PERMISSION.value: "No permission",
    ErrorCode.UNAUTHORIZED.value: "Invalid authentication credentials",
    ErrorCode.UNAUTHENTICATED.value: "Unauthenticated credentials",
    ErrorCode.INTERNAL_SERVER_ERROR: "Internal server error",
}
