from abc import abstractmethod, ABC
from app.models import Player
from datetime import datetime, timezone


class ICache(ABC):
    @abstractmethod
    def get_player(self, id: int) -> Player | None:
        raise NotImplementedError

    @abstractmethod
    def write_player(self, id: int, data: Player) -> bool:
        raise NotImplementedError

    @abstractmethod
    def cache_size(self) -> int:
        raise NotImplementedError


class DictCache(ICache):
    def __init__(self, ttl: int) -> None:
        self.ttl_sec = ttl
        self.__cache = {}

    def get_player(self, id: int) -> Player:
        player = self.__cache.get(id)
        if player != None:
            if (
                datetime.now(tz=timezone.utc) - player.get("timestamp")
            ).total_seconds() > self.ttl_sec:
                self.__cache.pop(id)
                return None
            player = player.get("player_info")
        return player

    def write_player(self, id: int, data: Player) -> bool:
        try:
            data = {"timestamp": datetime.now(tz=timezone.utc), "player_info": data}
            self.__cache[id] = data
            return True
        except:
            return False

    def cache_size(self) -> int:
        return len(self.__cache)
