import controllers
import uvicorn
from rapidapi.rapidapi import RapidAPI
from repositories.user_repository import UserRepository
from services.user_service import UserService
from settings import DatabaseSettings

if __name__ == "__main__":
    app = (
        RapidAPI()
        .register_settings(DatabaseSettings)
        .build_container(lambda container: container.factory(UserRepository).factory(UserService))
        .discover_controllers(controllers)
        .configure_logging(
            lambda builder: builder.register_middleware()
            .add_console_handler()
            .add_file_handler("logs/{time}.log"),
        )
        .load_plugins(lambda builder: builder.add_sqlite("sqlite://"))
        .build()
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)
