from api.pokeAPI import PokeAPIService, PokeAPIError
import pytest

poke_api_service = PokeAPIService()

def test_return_pikachu_data():

    response = poke_api_service.get_pokemon('pikachu')

    assert response.name == "pikachu"
    assert response.id == 25
    assert "electric" in [type for type in response.types]