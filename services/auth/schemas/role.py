from uuid import UUID

from pydantic import BaseModel


class RoleCreate(BaseModel):
    role: str


class RoleDelete(BaseModel):
    role_id: int


class RoleInDB(BaseModel):
    id: int
    role: str


class RoleAction(BaseModel):
    role_id: int
    user_id: UUID
