from typing import Any, Dict

import uvicorn
from trigon.core.controller import Controller, http, route
from trigon.core.controller.result import Ok, Result
from trigon.middlewares.logging import LoggingMiddleware
from trigon.trigon import trigon


class ItemService:
    def get_items(self) -> list[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "name": "Product 1",
                "description": "This is the description for Product 1.",
                "price": 19.99,
                "category": "Electronics",
                "stock": 50,
            },
            {
                "id": 2,
                "name": "Product 2",
                "description": "A sample description for Product 2.",
                "price": 29.99,
                "category": "Clothing",
                "stock": 100,
            },
            {
                "id": 3,
                "name": "Product 3",
                "description": "Description for Product 3 goes here.",
                "price": 9.99,
                "category": "Books",
                "stock": 25,
            },
        ]


class ItemController(Controller):
    def __init__(self, service: ItemService) -> None:
        self.service = service

    @route.get("/")
    @http.status(Ok)
    async def get_items(self) -> Result[list[Dict[str, Any]]]:
        return Ok(self.service.get_items())


if __name__ == "__main__":
    app = (
        trigon()
        .build_container(lambda builder: builder.singleton(ItemService))
        .register_controllers(ItemController)
        .configure_logging(
            lambda builder: builder.override("uvicorn.error", "uvicorn.asgi", "uvicorn.access")
            .add_console_handler()
            .add_file_handler("logs/{time}.log"),
        )
        .register_middlewares(LoggingMiddleware)
        .build()
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
