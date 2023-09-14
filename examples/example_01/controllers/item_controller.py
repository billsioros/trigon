from typing import Any, Dict

from services.item_service import ItemService
from trigon.core.controller import Controller, Ok, Result, http, route


class ItemController(Controller):
    def __init__(self, service: ItemService) -> None:
        self.service = service

    @route.get("/")
    @http.status(Ok)
    async def get_items(self) -> Result[list[Dict[str, Any]]]:
        return Ok(self.service.get_items())
