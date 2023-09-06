import controllers
import uvicorn
from rapidapi.rapidapi import RapidAPI
from services.item_service import ItemService

if __name__ == "__main__":
    app = (
        RapidAPI()
        .build_container(lambda container: container.singleton(ItemService))
        .discover_controllers(controllers)
        .configure_logging(
            lambda builder: builder.override("uvicorn")
            .register_middleware()
            .add_console_handler()
            .add_file_handler("logs/{time}.log"),
        )
        .build()
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
