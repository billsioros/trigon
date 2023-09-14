from pydantic import AnyUrl
from trigon.core.settings import Settings


class DatabaseSettings(Settings):
    url: AnyUrl = "sqlite://"
