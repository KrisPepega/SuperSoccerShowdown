import pytest
from pydantic import ValidationError
from app.models import Player, Team, TeamComposition
from typing import List


def test_player_valid():
    player = Player(name="name", weight_kg=11.1, height_cm=22.2)
    assert isinstance(player, Player)
    assert player.name == "name"
    assert player.weight_kg == 11.1
    assert player.height_cm == 22.2


def test_player_invalid():
    with pytest.raises(ValidationError):
        player = Player(name="name", weight_kg="asd", height_cm=22.2)

    with pytest.raises(ValidationError):
        player = Player(name=123, weight_kg=11.1, height_cm=22.2)

    with pytest.raises(ValidationError):
        player = Player(name="name", weight_kg=11.1, height_cm="asd")

    with pytest.raises(ValidationError):
        player = Player(weight_kg=11.1, height_cm=22.2)


def test_team_composition_default():
    team_comp = TeamComposition()
    assert isinstance(team_comp, TeamComposition)
    assert team_comp.size == 5
    assert team_comp.goalies == 1
    assert team_comp.offence == 2
    assert team_comp.defence == 2


def test_team_composition_valid():
    team_comp = TeamComposition(size=20, goalies=10, offence=5, defence=5)
    assert isinstance(team_comp, TeamComposition)
    assert team_comp.size == 20
    assert team_comp.goalies == 10
    assert team_comp.offence == 5
    assert team_comp.defence == 5


def test_team_composition_invalid():
    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1.1, goalies=10, offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size="asd", goalies=10, offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=[], goalies=10, offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size={}, goalies=10, offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, goalies=2.2, offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, goalies="asd", offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, goalies=[], offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, goalies={}, offence=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, offence=2.2, goalies=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, offence="asd", goalies=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, offence=[], goalies=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, offence={}, goalies=5, defence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, defence=2.2, goalies=5, offence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, defence="asd", goalies=5, offence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, defence=[], goalies=5, offence=5)

    with pytest.raises(ValidationError):
        team_comp = TeamComposition(size=1, defence={}, goalies=5, offence=5)


def test_team_valid():
    team = Team(
        players=[
            Player(name=f"name{i}", weight_kg=11.1, height_cm=111) for i in range(5)
        ],
        goalie=Player(name="goalie", weight_kg=11.1, height_cm=177.1),
        offence=[
            Player(name=f"offence{i}", weight_kg=11.1, height_cm=111) for i in range(2)
        ],
        defence=[
            Player(name=f"defence{i}", weight_kg=11.1, height_cm=111) for i in range(2)
        ],
    )
    assert isinstance(team, Team)
    assert isinstance(team.team_composition, TeamComposition)
    assert len(team.players) == 5
    assert len(team.defence) == 2
    assert len(team.offence) == 2
    assert isinstance(team.goalie, Player)
    assert isinstance(team.offence, List)
    assert isinstance(team.defence, List)
    assert isinstance(team.offence[0], Player)
    assert isinstance(team.offence[1], Player)
    assert isinstance(team.defence[0], Player)
    assert isinstance(team.defence[1], Player)


def test_team_invalid():
    with pytest.raises(ValidationError):
        team = Team(
            players="",
            goalie=Player(name="goalie", weight_kg=11.1, height_cm=177.1),
            offence=[
                Player(name=f"offence{i}", weight_kg=11.1, height_cm=111)
                for i in range(2)
            ],
            defence=[
                Player(name=f"defence{i}", weight_kg=11.1, height_cm=111)
                for i in range(2)
            ],
        )
