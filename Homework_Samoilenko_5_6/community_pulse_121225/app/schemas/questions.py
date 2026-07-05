from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, StringConstraints


QuestionText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]
CategoryName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: CategoryName


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: CategoryName | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class QuestionBase(BaseModel):
    text: QuestionText


class QuestionCreate(QuestionBase):
    category_id: int = Field(gt=0)


class QuestionUpdate(BaseModel):
    text: QuestionText | None = None
    category_id: int | None = Field(default=None, gt=0)


class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    category: CategoryBase