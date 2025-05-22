from typing import Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    error_code: int = 0
    message: str = ""


class BaseResponseData(BaseResponse):
    data: Union[dict, str, int, list, bool, None]
