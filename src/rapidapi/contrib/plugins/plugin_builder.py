from rapidapi.contrib.plugins import Plugin, database


class PluginBuilder:
    def __init__(self) -> None:
        self.plugins: list[Plugin] = []

    def _build(self) -> list[Plugin]:
        return self.plugins

    def add_sqlite(self, url: str):
        self.plugins.append(database.SQLitePlugin(url))

        return self
