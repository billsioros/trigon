import controllers
import uvicorn
from services.item_service import ItemService
from trigon.middlewares.logging import LoggingMiddleware
from trigon.trigon import trigon

if __name__ == "__main__":
    app = (
        trigon()
        .build_container(lambda container: container.singleton(ItemService))
        .discover_controllers(controllers)
        .configure_logging(
            lambda builder: builder.override("uvicorn.error", "uvicorn.asgi", "uvicorn.access")
            .add_console_handler()
            .add_file_handler("logs/{time}.log"),
        )
        .register_middlewares(LoggingMiddleware)
        .build()
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
