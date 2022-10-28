"""
In this example we had a function that was making a request to an external API.
We mocked the function so that it returns a static value instead of making the
actual request.
"""

import requests
import unittest

from unittest import mock


def get_all_pokemons():
    """Get all pokemons from external API."""
    return requests.get('https://pokeapi.co/api/v2/pokemon').json()


class PokemonService:
    """Pokemon service."""

    def get_all_pokemons(self):
        """Get all pokemons."""
        return get_all_pokemons()


class TestPokemonService(unittest.TestCase):
    """Test Pokemon service."""

    def setUp(self) -> None:
        self.pokemon_service = PokemonService()
        return super().setUp()

    @mock.patch('mock.get_all_pokemons')
    def test_get_all_pokemons(self, mock_get_all_pokemons):
        """Test get all pokemons."""
        mock_get_all_pokemons.return_value = {
            'results': [i for i in range(20)] # this mock data is far from real data but it's just an example
        }
        pokemons = self.pokemon_service.get_all_pokemons()
        self.assertEqual(len(pokemons['results']), 20)