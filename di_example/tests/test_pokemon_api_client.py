from unittest import TestCase

from app.main import PokemonAPIClientMock



class TestPokemonApiClient(TestCase):
    """Test Pokemon API client."""

    def setUp(self) -> None:
        self.pokemon_api_client = PokemonAPIClientMock()
        return super().setUp()

    def test_get_all_pokemons(self):
        """Test get all pokemons."""
        pokemons = self.pokemon_api_client.get_all_pokemons()
        self.assertEqual(len(pokemons['results']), 20) # this mock data is far from real data but it's just an example
