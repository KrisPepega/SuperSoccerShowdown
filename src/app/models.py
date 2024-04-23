from pydantic import BaseModel
from typing import List, Dict


class Player(BaseModel):
    name: str
    weight_kg: float
    height_cm: float


class TeamComposition(BaseModel):
    size: int = 5
    goalies: int = 1
    defence: int = 2
    offence: int = 2


class Team(BaseModel):
    team_composition: TeamComposition = TeamComposition()
    players: List[Player]
    goalie: Player
    defence: List[Player]
    offence: List[Player]
