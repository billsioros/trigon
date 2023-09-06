from schemas import Schema


class Permission(Schema):
    class Config:
        from_attributes = True

    id: str
    name: str


class User(Schema):
    class Config:
        from_attributes = True

    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    active: bool


class UserCreate(Schema):
    class Config:
        from_attributes = True

    username: str
    email: str
    first_name: str
    last_name: str
