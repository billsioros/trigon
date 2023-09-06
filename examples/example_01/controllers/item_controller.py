from typing import Any, Dict

from rapidapi.core.controller import Controller, get
from services.item_service import ItemService


class ItemController(Controller):
    def __init__(self, service: ItemService) -> None:
        super().__init__()

        self.service = service

    @get("/")
    def get_items(self) -> list[Dict[str, Any]]:
        return self.service.get_items()
