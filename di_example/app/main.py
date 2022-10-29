import requests

from abc import ABC, abstractmethod

# I've made this an abstract class so that we can mock it in our tests and assure
# that we implement the same interface with our mock.
class IPokemonAPIClient(ABC): 
    """Pokemon API client interface."""
    @abstractmethod
    def get_all_pokemons(self):
        """Get all pokemons from external API."""
        raise NotImplementedError('You must implement this method.')


class PokemonAPIClient(IPokemonAPIClient):
    """Pokemon API client."""

    def __init__(self, api_url: str, timeout: int) -> None:
        self.url = api_url
        self.timeout = timeout

    def __init__(self,) -> None:
        pass

    def get_all_pokemons(self) -> dict:
        """Get all pokemons from external API."""
        return requests.get('https://pokeapi.co/api/v2/pokemon').json()


class PokemonAPIClientMock(IPokemonAPIClient):
    """Pokemon API client mock."""

    def get_all_pokemons(self) -> dict:
        """Get all pokemons from external API."""
        return {
            'results': [i for i in range(20)]
        }


