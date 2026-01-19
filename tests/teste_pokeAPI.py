from api.pokeAPI import PokeAPIService, PokeAPIError
import pytest

poke_api_service = PokeAPIService()

def test_return_pikachu_data():

    response = poke_api_service.get_pokemon('pikachu')
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "pikachu"
    assert data["id"] == 25
    assert "electric" in [type_info["type"]["name"] for type_info in data["types"]]