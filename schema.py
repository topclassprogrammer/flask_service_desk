from pydantic import BaseModel, field_validator


class CreateTicket(BaseModel):
    topic: str
    description: str
    status: str
    user: int


class BaseUser(BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters')
        return value

class CreateUser(BaseUser):
    username: str
    password: str


class UpdateUser(BaseUser):
    username: str | None = None
    password: str | None = None



