from __future__ import annotations
import logging
from dataclasses import dataclass
from pydantic_settings import BaseSettings
from functools import wraps
from typing import Any, Callable, Coroutine, Optional
from typing_extensions import ParamSpec
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field


class Chat_request(BaseModel):
    user_input: str = "生成一段用java寫數字list排序的程式碼"
    history: list = []

class Chat_response(BaseModel):
    generate_text: str 
    history: list

class HTTPErrorResult(BaseModel):
    result: int

class HTTPSuccessResult(BaseModel):
    message: str

@dataclass
class Errors:
    NO_INPUT_ERROR = JSONResponse({'result':3}, 400)
    INTERNAL_ERROR = JSONResponse({'result':999}, 500)


logger = logging.getLogger('uvicorn.error')
P = ParamSpec('P')

def catch_error(func: Callable[P, Coroutine[Any, Any, Any]]) -> Callable[P, Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            logger.error(str(ex), exc_info=True, stack_info=True)
            return Errors.INTERNAL_ERROR

    return wrapper