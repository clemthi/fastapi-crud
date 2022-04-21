from pydantic import BaseModel


class ScoreDescription(BaseModel):
    name: str
    label: str
    description: str
