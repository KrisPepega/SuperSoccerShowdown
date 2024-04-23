import uvicorn
from fastapi import FastAPI
import os

from app.cache import DictCache
from app.universe_handler import PokemonHandler, StarwarsHandler
from app.models import Team

DEBUG = os.getenv("POKEMON_API")
DEV_MODE = os.getenv("DEV_MODE")

app = FastAPI()

pokemon_in_mem_cache = DictCache(ttl=86400)
pokemon_handler = PokemonHandler(
    api_str=os.getenv("POKEMON_API"), cache=pokemon_in_mem_cache, debug=DEBUG
)

starwars_in_mem_cache = DictCache(ttl=86400)
starwars_handler = StarwarsHandler(
    api_str=os.getenv("ALT_STARWARS_API"), cache=starwars_in_mem_cache, debug=DEBUG
)


@app.get("/random_pokemon_team", status_code=200)
def get_random_pokemon_team() -> Team:
    return pokemon_handler.get_random_team()


@app.get("/random_starwars_team", status_code=200)
def get_random_starwars_team() -> Team:
    return starwars_handler.get_random_team()


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=DEV_MODE)
