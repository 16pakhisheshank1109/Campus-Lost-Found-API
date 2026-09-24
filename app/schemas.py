from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

ItemStatus = Literal["Lost", "Found", "Returned"]


class ItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=3)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: ItemStatus

    @field_validator(
        "title",
        "description",
        "category",
        "location",
        "reported_by",
    )
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field must not be empty")
        return value


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=3)
    category: Optional[str] = Field(default=None, min_length=1)
    location: Optional[str] = Field(default=None, min_length=1)
    reported_by: Optional[str] = Field(default=None, min_length=1)
    status: Optional[ItemStatus] = None

    @field_validator(
        "title",
        "description",
        "category",
        "location",
        "reported_by",
    )
    @classmethod
    def validate_text(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Field must not be empty")
        return value