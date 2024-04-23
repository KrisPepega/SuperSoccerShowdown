from datetime import datetime, timedelta, timezone
import pytest
from app.cache import DictCache
from app.models import Player


def test_cache_write():
    cache = DictCache(60)
    player_data = Player(name="name", weight_kg=11.1, height_cm=22.2)
    assert cache.write_player(1, player_data)
    assert cache.cache_size() == 1
    assert cache.get_player(1) == player_data


def test_cache_read_exists():
    cache = DictCache(60)
    player_data = Player(name="name", weight_kg=11.1, height_cm=22.2)
    cache.write_player(1, player_data)
    assert cache.get_player(1) != None


def test_cache_read_not_exists():
    cache = DictCache(60)
    assert cache.get_player(1) == None


def test_get_expired_player():
    cache = DictCache(10)
    player_data = Player(name="name", weight_kg=11.1, height_cm=22.2)
    cache.write_player(1, player_data)

    time = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - time).total_seconds() < 10:
        pass

    assert cache.get_player(1) is None


def test_cache_size():
    cache = DictCache(60)
    player_data = Player(name="name", weight_kg=11.1, height_cm=22.2)

    cache.write_player(1, player_data)
    cache.write_player(2, player_data)
    cache.write_player(3, player_data)

    assert cache.cache_size() == 3
