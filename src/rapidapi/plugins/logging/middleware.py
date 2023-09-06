from fastapi.responses import JSONResponse
from loguru import logger
from starlette import status
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from rapidapi.core.middleware import Middleware


class LoggingMiddleware(Middleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            logger.debug(f"{request.method} {request.url}")

            response = await call_next(request)

            logger.debug(f"{request.method} {request.url} {response.status_code}")
        except Exception as exception:  # noqa: BLE001
            logger.exception(exception)

            return JSONResponse(
                {"message": "Internal Server Error", "detail": str(exception)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response
