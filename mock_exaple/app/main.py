"""
In this example we had a function that was making a request to an external API.
We need to mock the function so that it returns a static value instead of making the
actual request.
"""

import requests


def get_all_pokemons():
    """Get all pokemons from external API."""
    return requests.get('https://pokeapi.co/api/v2/pokemon').json()


class PokemonService:
    """Pokemon service."""

    def get_all_pokemons(self):
        """Get all pokemons."""
        return get_all_pokemons()


def main():
    """Main function."""
    pokemon_service = PokemonService()
    pokemons = pokemon_service.get_all_pokemons()
    print(pokemons)

if __name__ == '__main__':
    main()