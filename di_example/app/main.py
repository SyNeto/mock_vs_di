""" This example is far more complex than the previous one, but it's more realistic.
and it will help tho shows how to unittest injecting our mocks depending on the 
environment (develop/test will use our mocks).
"""
from email.policy import default
import requests

from abc import ABC, abstractmethod
from dependency_injector import containers, providers

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
        self.api_url = api_url
        self.timeout = timeout

    def get_all_pokemons(self) -> dict:
        """Get all pokemons from external API."""
        return requests.get(
            url=self.api_url,
            timeout=self.timeout).json()


class PokemonAPIClientMock(IPokemonAPIClient):
    """Pokemon API client mock."""

    def get_all_pokemons(self) -> dict:
        """Get all pokemons from external API."""
        return {
            'results': [i for i in range(20)]
        }


class PokemonService:
    """Pokemon service."""

    def __init__(self, pokemon_api_client: IPokemonAPIClient):
        """Initialize Pokenmon service.
        The dependency injection is not only helpful for testing, but also
        for decoupling our code.
        
        This way we can easily change our Pokemon API client for another one
        if we need to.
        
        take as example the PokemonAPIClientMock, we can easily change it for
        other client that implements the same interface."""
        self.pokemon_api_client = pokemon_api_client

    def get_all_pokemons(self):
        """Get all pokemons."""
        return self.pokemon_api_client.get_all_pokemons()


class Container(containers.DeclarativeContainer):
    """Container.
    provides the dependency injection.
    This container will be used to inject our dependencies.
    """

    config = providers.Configuration()

    pokemon_api_client = providers.Singleton(
        PokemonAPIClient,
        api_url=config.api_url,
        timeout=config.timeout,
    )

    pokemon_service = providers.Factory(
        PokemonService,
        pokemon_api_client=pokemon_api_client,
    )


def pokemon_service_factory(app_env:str=None) -> PokemonService:
    """Pokemon service factory."""
    container = Container()
    if app_env:
        container.config.env.from_env('APP_ENV', default=app_env)
    else:
        container.config.env.from_env('APP_ENV', default='develop')
    container.config.api_url.from_env('POKEMON_API_URL', default='https://pokeapi.co/api/v2/pokemon')
    container.config.timeout.from_env('REQUEST_TIMEOUT', default=5)
    container.wire(modules=[__name__])
    if container.config.env() == 'test':
        print('Using mock for Pokemon API client')
        container.pokemon_api_client.override(PokemonAPIClientMock())

    return container.pokemon_service()


if __name__ == '__main__':
    """Startup code."""

    pokemon_service = pokemon_service_factory()
    print(pokemon_service.get_all_pokemons())
