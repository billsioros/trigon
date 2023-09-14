import controllers
import uvicorn
from models import Model
from repositories.user_repository import UserRepository
from services.user_service import UserService
from trigon.contrib.plugins.database import SQLitePlugin
from trigon.middlewares.logging import LoggingMiddleware
from trigon.trigon import trigon

if __name__ == "__main__":
    app = (
        trigon()
        .build_container(lambda container: container.factory(UserRepository).factory(UserService))
        .discover_controllers(controllers)
        .configure_logging(
            lambda builder: builder.override("uvicorn.error", "uvicorn.asgi", "uvicorn.access")
            .add_console_handler()
            .add_file_handler("logs/{time}.log"),
        )
        .register_middlewares(LoggingMiddleware)
        .load_plugins(lambda builder: builder.add(SQLitePlugin("sqlite://", Model)))
        .build()
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
