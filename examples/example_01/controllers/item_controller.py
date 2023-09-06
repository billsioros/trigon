from typing import Any, Dict

from rapidapi.core.controller import Controller, Ok, Result, http, route
from services.item_service import ItemService


class ItemController(Controller):
    def __init__(self, service: ItemService) -> None:
        self.service = service

    @route.get("/")
    @http.status(Ok)
    async def get_items(self) -> Result[list[Dict[str, Any]]]:
        return Ok(self.service.get_items())
