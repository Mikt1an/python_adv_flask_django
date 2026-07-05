from pydantic import BaseModel

from app.schemas.questions import CategoryCreate, CategoryUpdate, CategoryRead


class CategoryCreateRequest(CategoryCreate):
    pass


class CategoryUpdateRequest(CategoryUpdate):
    pass


class CategoryResponse(CategoryRead):
    pass


class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]
    count: int