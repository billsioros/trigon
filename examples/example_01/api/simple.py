import uvicorn
from rapidapi.core.controller import Controller, get
from rapidapi.middlewares.correlation_id import CorrelationIdMiddleware
from rapidapi.plugins.logging.logging import LoggingMiddleware
from lagom import Container
from rapidapi.rapidapi import RapidAPI

if __name__ == "__main__":

    class SomeService:
        def __init__(self) -> None:
            self.items = ["asdf", "Asdfa"]

    class ItemsController(Controller):
        def __init__(self, service: SomeService) -> None:
            super().__init__()

            self.service = service

        @get('/')
        def get_items(self) -> list[str]:
            return self.service.items

    def construct_container(container: Container):
        container[SomeService] = SomeService()
        container[ItemsController] = lambda container: ItemsController(container[SomeService])

        return container

    app = (
        RapidAPI()
        .configure()
        .register_container(construct_container)
        .register_controllers(ItemsController)
        # .register_middlewares([CorrelationIdMiddleware, LoggingMiddleware])
        .build()
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
