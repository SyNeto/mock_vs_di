import unittest

from unittest import mock

from app.main import PokemonService


class TestPokemonService(unittest.TestCase):
    """Test Pokemon service."""

    def setUp(self) -> None:
        self.pokemon_service = PokemonService()
        return super().setUp()

    @mock.patch('app.main.get_all_pokemons')
    def test_get_all_pokemons(self, mock_get_all_pokemons):
        """Test get all pokemons."""
        mock_get_all_pokemons.return_value = {
            'results': [i for i in range(20)] # this mock data is far from real data but it's just an example
        }
        pokemons = self.pokemon_service.get_all_pokemons()
        self.assertEqual(len(pokemons['results']), 20)

