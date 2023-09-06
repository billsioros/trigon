from pydantic import AnyUrl
from rapidapi.core.settings import Settings


class DatabaseSettings(Settings):
    url: AnyUrl = "sqlite://"
