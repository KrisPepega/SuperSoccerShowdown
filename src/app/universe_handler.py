from abc import ABC, abstractmethod
import random
import requests
from app.models import Player, Team, TeamComposition
from app.cache import ICache


class BaseHandler(ABC):
    def __init__(self, api_str: str, cache: ICache, debug: bool = False) -> None:
        self.api_str = api_str
        self.cache = cache
        self.debug = debug
        self.total = -1

    def get_random_team(self) -> Team:
        if self.debug:
            print(f"cache size - {self.cache.cache_size()}")

        team_comp = TeamComposition()
        players = []
        goalie_index = -1
        goalie = None
        unique_random_ids = random.sample(range(1, self.total + 1), team_comp.size)

        for i, id in enumerate(unique_random_ids):
            player = self.get_from_cache(id)
            if goalie_index == -1:
                goalie = player
                goalie_index = i
            elif player.height_cm > goalie.height_cm or (
                player.height_cm == goalie.height_cm
                and player.weight_kg < goalie.weight_kg
            ):
                goalie = player
                goalie_index = i
            players.append(player)

        players_copy = players.copy()
        players_copy.pop(goalie_index)
        players_copy.sort(key=lambda p: (p.weight_kg, p.height_cm))

        return Team(
            team_composition=team_comp,
            players=players,
            goalie=goalie,
            defence=[players_copy[-2], players_copy[-1]],
            offence=[players_copy[0], players_copy[1]],
        )

    def get_from_api(self, id: int) -> Player | None:
        if self.debug:
            print(f"API CALL - ID: {id}")
        query = f"{self.api_str}/{id}"
        try:
            r = requests.get(query)
            r.raise_for_status()
            return self.convert_to_player(r.json())
        except requests.exceptions.HTTPError as e:
            print(e)
            return None

    def get_from_cache(self, id: int) -> Player | None:
        cached_player = self.cache.get_player(id)
        if cached_player == None:
            if self.debug:
                print("CACHE MISS")
            player = self.get_from_api(id)
            if player != None:
                self.cache.write_player(id, player)
            return player
        if self.debug:
            print("CACHE HIT")
        return cached_player

    @abstractmethod
    def convert_to_player(self, entity: dict) -> Player:
        raise NotImplementedError

    @abstractmethod
    def update_total(self) -> None:
        raise NotImplementedError


class PokemonHandler(BaseHandler):
    def __init__(self, api_str: str, cache: ICache, debug: bool = False) -> None:
        super().__init__(api_str, cache, debug)
        self.update_total()

    def convert_to_player(self, entity: dict) -> Player:
        return Player(
            name=entity["name"],
            weight_kg=entity["weight"] / 10,
            height_cm=entity["height"] * 10,
        )

    def update_total(self):
        # r = requests.get(f"{self.api_str}?limit=1").json()
        # self.total = r["count"]
        self.total = 1025


class StarwarsHandler(BaseHandler):
    def __init__(self, api_str: str, cache: ICache, debug: bool = False) -> None:
        super().__init__(api_str, cache, debug)
        self.update_total()

    def convert_to_player(self, entity: dict) -> Player:
        return Player(
            name=entity["name"] if entity["name"] != "unknown" else "-1",
            weight_kg=(
                entity["mass"].replace(",", "") if entity["mass"] != "unknown" else -1
            ),
            height_cm=(
                entity["height"].replace(",", "")
                if entity["height"] != "unknown"
                else -1
            ),
        )

    def update_total(self) -> None:
        r = requests.get(f"{self.api_str}").json()
        self.total = r["count"]
