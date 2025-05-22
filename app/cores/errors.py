from fastapi import HTTPException


class PermissionDeniedException(Exception):
    pass


class NotFoundException(Exception):
    pass


class ConflictException(Exception):
    pass


class BadRequestException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class UnauthorizedException(HTTPException):
    pass
