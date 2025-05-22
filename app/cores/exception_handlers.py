import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.constants.error import ERROR_MESSAGES, ErrorCode
from app.cores.errors import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    PermissionDeniedException,
)
from app.dto.response_dto import BaseResponseData

_logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def request_validator_handler(request: Request, exc: ValidationError):
        error_code = str(exc)
        _logger.warning(f"RequestValidationError error_code: {error_code}")
        return JSONResponse(
            status_code=422,
            content=BaseResponseData(
                error_code=422, message=error_code, data=None
            ).model_dump(),
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_handler(request: Request, exc: BadRequestException):
        error_code = str(exc)
        _logger.warning(f"BadRequestException error_code: {error_code}")
        return JSONResponse(
            status_code=400,
            content=BaseResponseData(
                error_code=error_code, message=ERROR_MESSAGES[error_code], data=None
            ).model_dump(),
        )

    @app.exception_handler(PermissionDeniedException)
    async def permission_denied_handler(
        request: Request, exc: PermissionDeniedException
    ):
        error_code = str(exc)
        _logger.warning(f"PermissionDeniedException error_code: {error_code}")
        return JSONResponse(
            status_code=401,
            content=BaseResponseData(
                error_code=error_code, message=ERROR_MESSAGES[error_code], data=None
            ).model_dump(),
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        error_code = str(exc)
        _logger.warning(f"NotFoundException error_code: {error_code}")
        return JSONResponse(
            status_code=404,
            content=BaseResponseData(
                error_code=error_code, message=ERROR_MESSAGES[error_code], data=None
            ).model_dump(),
        )

    @app.exception_handler(ConflictException)
    async def conflict_handler(request: Request, exc: ConflictException):
        error_code = str(exc)
        _logger.warning(f"ConflictException error_code: {error_code}")
        return JSONResponse(
            status_code=469,
            content=BaseResponseData(
                error_code=error_code, message=ERROR_MESSAGES[error_code], data=None
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        _logger.error(f"Unhandled server error {str(exc)}")
        return JSONResponse(
            status_code=500,
            content=BaseResponseData(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR.value,
                message="Internal Server Error",
                data=None,
            ).model_dump(),
        )
