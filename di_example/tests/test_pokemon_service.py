from unittest import TestCase

from app.main import pokemon_service_factory


class TestPokemonService(TestCase):
    """Test Pokemon service."""

    def setUp(self) -> None:
        self.pokemon_service = pokemon_service_factory(app_env='test')
        return super().setUp()

    def test_get_all_pokemons(self):
        """Test get all pokemons."""
        pokemons = self.pokemon_service.get_all_pokemons()
        self.assertEqual(len(pokemons['results']), 20) # this mock data is far from real data but it's just an example
