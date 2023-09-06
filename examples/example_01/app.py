import controllers
import uvicorn
from rapidapi.core.dependency_injection import Container
from rapidapi.plugins.logging import LoggingPlugin
from rapidapi.rapidapi import RapidAPI
from services.item_service import ItemService

if __name__ == "__main__":
    app = (
        RapidAPI()
        .configure()
        .register_container(Container().singleton(ItemService()))
        .discover_controllers(controllers)
        .register_plugins(LoggingPlugin())
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
