from contextvars import ContextVar
from uuid import uuid4

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from rapidapi.middlewares import Middleware

CORRELATION_ID_CTX_KEY = "correlation_id"

_correlation_id_ctx_var: ContextVar[str] = ContextVar(CORRELATION_ID_CTX_KEY, default=None)


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


class CorrelationIdMiddleware(Middleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = _correlation_id_ctx_var.set(
            request.headers.get("X-Correlation-ID", str(uuid4())),
        )

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = get_correlation_id()

        _correlation_id_ctx_var.reset(correlation_id)

        return response
