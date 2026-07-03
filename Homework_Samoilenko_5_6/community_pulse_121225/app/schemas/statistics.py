from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, computed_field


class StatisticsRead(BaseModel):
    question_id: int
    agree_count: int
    disagree_count: int

    @computed_field
    @property
    def total_count(self) -> int:
        return self.agree_count + self.disagree_count