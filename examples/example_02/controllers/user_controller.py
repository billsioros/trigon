from schemas.user import User, UserCreate
from services.user_service import UserService
from trigon.core.controller import Controller, http, route
from trigon.core.controller.result import Created, Error, NoContent, NotFound, Ok, Result


# TODO: async
class UserController(Controller):
    def __init__(self, user_service: UserService) -> None:
        self.user_service: UserService = user_service

    @route.get("/")
    @http.status(Ok)
    async def get_all(self) -> Result[list[User]]:
        user_result = self.user_service.get_all()

        return Ok(user_result.payload)

    @route.get("/{id}")
    @http.status(NotFound, model=Error)
    @http.status(Ok, model=User)
    async def get_by_id(self, id: str) -> Result[User]:
        user_result = self.user_service.get_by_id(id)

        if not user_result:
            return NotFound(f"No user with an id of {id}")

        return Ok(user_result.payload)

    @route.post("/")
    @http.status(Created, model=User)
    async def create(self, user_create: UserCreate) -> Result[User]:
        user_result = self.user_service.create(user_create)

        return Created(user_result.payload)

    @route.delete("/{id}")
    @http.status(NoContent, model=None)
    async def delete(self, id: str) -> Result[None]:
        self.user_service.delete(id)

        return NoContent()
