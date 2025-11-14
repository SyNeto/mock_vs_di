"""Dependency Injection testing example.

This example is far more complex than the previous one, but it's more realistic.
It shows how to unittest injecting our mocks depending on the
environment (develop/test will use our mocks).
"""
import requests
from typing import Dict, Any, Optional

from abc import ABC, abstractmethod
from dependency_injector import containers, providers

# I've made this an abstract class so that we can mock it in our tests and assure
# that we implement the same interface with our mock.
class IPokemonAPIClient(ABC):
    """Pokemon API client interface.

    This interface defines the contract that all Pokemon API clients must follow,
    allowing for easy substitution between real and mock implementations.
    """
    @abstractmethod
    def get_all_pokemons(self) -> Dict[str, Any]:
        """Get all pokemons from external API.

        Returns:
            Dict containing the API response with pokemon data.
        """
        raise NotImplementedError('You must implement this method.')


class PokemonAPIClient(IPokemonAPIClient):
    """Pokemon API client that makes real HTTP requests.

    This implementation connects to the actual Pokemon API to retrieve data.
    """

    def __init__(self, api_url: str, timeout: int) -> None:
        """Initialize the Pokemon API client.

        Args:
            api_url: The base URL for the Pokemon API.
            timeout: Request timeout in seconds.
        """
        self.api_url = api_url
        self.timeout = timeout

    def get_all_pokemons(self) -> Dict[str, Any]:
        """Get all pokemons from external API.

        Returns:
            Dict containing the API response with pokemon data.
        """
        return requests.get(
            url=self.api_url,
            timeout=self.timeout).json()


class PokemonAPIClientMock(IPokemonAPIClient):
    """Pokemon API client mock for testing.

    This mock implementation returns static data that resembles the actual
    Pokemon API response structure, without making real HTTP requests.
    """

    def get_all_pokemons(self) -> Dict[str, Any]:
        """Get mock pokemon data.

        Returns:
            Dict containing mock pokemon data with the same structure as the real API.
        """
        return {
            'count': 1292,
            'next': 'https://pokeapi.co/api/v2/pokemon?offset=20&limit=20',
            'previous': None,
            'results': [
                {'name': 'bulbasaur', 'url': 'https://pokeapi.co/api/v2/pokemon/1/'},
                {'name': 'ivysaur', 'url': 'https://pokeapi.co/api/v2/pokemon/2/'},
                {'name': 'venusaur', 'url': 'https://pokeapi.co/api/v2/pokemon/3/'},
                {'name': 'charmander', 'url': 'https://pokeapi.co/api/v2/pokemon/4/'},
                {'name': 'charmeleon', 'url': 'https://pokeapi.co/api/v2/pokemon/5/'},
                {'name': 'charizard', 'url': 'https://pokeapi.co/api/v2/pokemon/6/'},
                {'name': 'squirtle', 'url': 'https://pokeapi.co/api/v2/pokemon/7/'},
                {'name': 'wartortle', 'url': 'https://pokeapi.co/api/v2/pokemon/8/'},
                {'name': 'blastoise', 'url': 'https://pokeapi.co/api/v2/pokemon/9/'},
                {'name': 'caterpie', 'url': 'https://pokeapi.co/api/v2/pokemon/10/'},
            ]
        }


class PokemonService:
    """Pokemon service that uses dependency injection.

    This service receives its dependencies through constructor injection,
    making it easy to test and maintain.
    """

    def __init__(self, pokemon_api_client: IPokemonAPIClient) -> None:
        """Initialize Pokemon service.

        The dependency injection is not only helpful for testing, but also
        for decoupling our code.

        This way we can easily change our Pokemon API client for another one
        if we need to.

        Take as example the PokemonAPIClientMock, we can easily change it for
        another client that implements the same interface.

        Args:
            pokemon_api_client: An implementation of IPokemonAPIClient interface.
        """
        self.pokemon_api_client = pokemon_api_client

    def get_all_pokemons(self) -> Dict[str, Any]:
        """Get all pokemons.

        Returns:
            Dict containing the API response with pokemon data.
        """
        return self.pokemon_api_client.get_all_pokemons()


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container.

    This container provides the dependency injection configuration.
    It will be used to wire up and inject our dependencies throughout the application.

    The container uses:
    - Singleton pattern for the API client (single instance shared across the app)
    - Factory pattern for the service (new instance each time it's requested)
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


def pokemon_service_factory(app_env: Optional[str] = None) -> PokemonService:
    """Factory function to create a configured PokemonService instance.

    This factory:
    1. Creates and configures the DI container
    2. Loads configuration from environment variables
    3. Switches to mock implementation in test environment
    4. Returns a fully wired PokemonService instance

    Args:
        app_env: Optional environment override ('test', 'develop', 'production').
                If not provided, reads from APP_ENV environment variable.

    Returns:
        A configured PokemonService instance.
    """
    container = Container()

    # Configure environment
    container.config.env.from_env('APP_ENV', default=app_env or 'develop')

    # Configure API settings
    container.config.api_url.from_env(
        'POKEMON_API_URL',
        default='https://pokeapi.co/api/v2/pokemon'
    )
    container.config.timeout.from_env('REQUEST_TIMEOUT', default=5)

    # Wire the container
    container.wire(modules=[__name__])

    # Use mock in test environment
    if container.config.env() == 'test':
        print('Using mock for Pokemon API client')
        container.pokemon_api_client.override(PokemonAPIClientMock())

    return container.pokemon_service()


if __name__ == '__main__':
    """Startup code to demonstrate the DI example."""
    pokemon_service = pokemon_service_factory()
    print(pokemon_service.get_all_pokemons())
