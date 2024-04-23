import pytest
import json
from unittest.mock import patch, MagicMock
from app.cache import ICache
from app.models import Player, Team, TeamComposition
from app.universe_handler import PokemonHandler, StarwarsHandler


class MockCache(ICache):
    def __init__(self):
        self.__cache = {}

    def get_player(self, id: int) -> Player:
        return self.__cache.get(id)

    def write_player(self, id: int, data: Player) -> bool:
        self.__cache[id] = data
        return True

    def cache_size(self) -> int:
        return len(self.__cache)


@pytest.fixture
def mock_cache():
    return MockCache()


def test_get_from_api_valid_poke(mock_cache):
    handler = PokemonHandler(
        api_str="https://example.com", cache=mock_cache, debug=False
    )
    with patch("app.universe_handler.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "John",
            "weight": 70,
            "height": 180,
        }
        player = handler.get_from_api(1)
        assert player.name == "John"


def test_get_valid_id_from_cache(mock_cache):
    mock_cache.write_player(1, Player(name="John", weight_kg=70.0, height_cm=180.0))
    handler = PokemonHandler(
        api_str="https://example.com", cache=mock_cache, debug=False
    )
    player = handler.get_from_cache(1)
    assert player.name == "John"


def test_get_invalid_id_from_cache(mock_cache):
    handler = PokemonHandler(
        api_str="https://example.com", cache=mock_cache, debug=False
    )
    player = handler.get_from_cache(1)
    assert player == None


def test_convert_to_player_pokemon(mock_cache):
    handler = PokemonHandler(
        api_str="https://example.com", cache=mock_cache, debug=False
    )
    entity = {"name": "Pikachu", "weight": 60, "height": 4}
    player = handler.convert_to_player(entity)
    assert player.name == "Pikachu"
    assert player.weight_kg == 6.0
    assert player.height_cm == 40


def test_convert_to_player_starwars(mock_cache):
    with patch("app.universe_handler.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"count": 10}
        handler = StarwarsHandler(
            api_str="https://example.com", cache=mock_cache, debug=False
        )
        entity = {"name": "Luke Skywalker", "mass": "70", "height": "180"}
        player = handler.convert_to_player(entity)
        assert player.name == "Luke Skywalker"
        assert player.weight_kg == 70
        assert player.height_cm == 180


def test_update_total_pokemon(mock_cache):
    handler = PokemonHandler(
        api_str="https://example.com", cache=mock_cache, debug=False
    )
    handler.update_total()
    assert handler.total == 1025


def test_update_total_starwars(mock_cache):
    with patch("app.universe_handler.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"count": 10}
        handler = StarwarsHandler(
            api_str="https://example.com", cache=mock_cache, debug=False
        )
        assert handler.total == 10


def test_pokemon_team_generator(mock_cache):
    poke_handler = PokemonHandler(
        api_str="https://example.com", cache=mock_cache, debug=False
    )
    poke_handler.get_from_cache = MagicMock(
        return_value=Player(name="Player1", weight_kg=70.0, height_cm=180.0)
    )

    team = poke_handler.get_random_team()

    assert isinstance(team, Team)
    assert len(team.players) == 5
    assert isinstance(team.goalie, Player)
    assert len(team.defence) == 2
    assert len(team.offence) == 2
