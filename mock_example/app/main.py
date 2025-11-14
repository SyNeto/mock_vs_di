"""Mock-based testing example.

In this example we have a function that makes a request to an external API.
We need to mock the function so that it returns a static value instead of making
the actual request.

This approach uses Python's unittest.mock to patch the function at test time.
"""

import requests
from typing import Dict, Any


def get_all_pokemons() -> Dict[str, Any]:
    """Get all pokemons from external API.

    Returns:
        Dict containing the API response with pokemon data.
    """
    return requests.get('https://pokeapi.co/api/v2/pokemon').json()


class PokemonService:
    """Pokemon service that uses the global get_all_pokemons function.

    This class demonstrates the traditional approach where dependencies
    are called directly as global functions.
    """

    def get_all_pokemons(self) -> Dict[str, Any]:
        """Get all pokemons.

        Returns:
            Dict containing the API response with pokemon data.
        """
        return get_all_pokemons()


def main() -> None:
    """Main function to demonstrate the service usage."""
    pokemon_service = PokemonService()
    pokemons = pokemon_service.get_all_pokemons()
    print(pokemons)

if __name__ == '__main__':
    main()
