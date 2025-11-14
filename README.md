# Mock vs Dependency Injection (DI)

A practical comparison of two popular testing approaches in Python: Mock-based testing and Dependency Injection-based testing.

## Overview

This repository demonstrates the differences between two approaches to testing code that depends on external services:

1. **Mock-based testing**: Using `unittest.mock` to patch functions and methods at test time
2. **Dependency Injection (DI)**: Using the `dependency-injector` library to inject dependencies through constructors

Both examples use a Pokemon API client to illustrate how to test code that makes external HTTP requests without actually calling the API during tests.

## Project Structure

```
mock_vs_di/
├── mock_example/           # Traditional mock-based approach
│   ├── app/
│   │   └── main.py        # Simple implementation using global functions
│   └── tests/
│       └── test_pokemon_service.py  # Tests using @mock.patch
│
├── di_example/            # Dependency Injection approach
│   ├── app/
│   │   └── main.py        # Advanced implementation with DI container
│   └── tests/
│       ├── test_pokemon_api_client.py  # Tests for mock client
│       └── test_pokemon_service.py     # Tests using DI factory
│
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
└── README.md             # This file
```

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/mock_vs_di.git
cd mock_vs_di
```

### Install dependencies

For production:
```bash
pip install -r requirements.txt
```

For development (includes testing and linting tools):
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Usage

### Running the Mock Example

```bash
# Run the application
python -m mock_example.app.main

# Run tests
python -m pytest mock_example/tests/
```

### Running the DI Example

```bash
# Run the application (uses real API)
python -m di_example.app.main

# Run tests (uses mock)
APP_ENV=test python -m pytest di_example/tests/

# Or use the factory with environment parameter
python -m di_example.app.main
```

### Environment Variables

The DI example supports configuration through environment variables:

- `APP_ENV`: Environment mode (`develop`, `test`, `production`)
- `POKEMON_API_URL`: Pokemon API endpoint (default: `https://pokeapi.co/api/v2/pokemon`)
- `REQUEST_TIMEOUT`: HTTP request timeout in seconds (default: `5`)

Example:
```bash
export APP_ENV=test
export POKEMON_API_URL=https://pokeapi.co/api/v2/pokemon
export REQUEST_TIMEOUT=10
python -m di_example.app.main
```

## Comparison: Mock vs Dependency Injection

### Mock-Based Testing

**How it works:**
- Uses `@mock.patch` decorator to replace functions/methods at runtime
- Patches are applied at the module level using import paths
- Mock configuration happens in test files

**Example:**
```python
@mock.patch('app.main.get_all_pokemons')
def test_get_all_pokemons(self, mock_get_all_pokemons):
    mock_get_all_pokemons.return_value = {'results': [...]}
    service = PokemonService()
    result = service.get_all_pokemons()
```

### Dependency Injection Testing

**How it works:**
- Dependencies are passed through constructors (constructor injection)
- Uses interfaces (ABC) to define contracts
- Container manages object creation and wiring
- Environment-based configuration switches between real and mock implementations

**Example:**
```python
def test_get_all_pokemons(self):
    pokemon_service = pokemon_service_factory(app_env='test')
    pokemons = pokemon_service.get_all_pokemons()
```

## Pros and Cons

### Mock-Based Testing

**Pros:**
- Simple and straightforward
- Minimal upfront setup
- No architectural changes required
- Good for legacy code
- Part of Python's standard library

**Cons:**
- Tight coupling to implementation details (import paths)
- Harder to refactor (patches break when code moves)
- Mock configuration scattered in test files
- No compile-time/type safety
- Can lead to brittle tests

### Dependency Injection Testing

**Pros:**
- Loose coupling between components
- Easy to refactor (interface-based)
- Type-safe (interface enforcement via ABC)
- Mock implementations are reusable production code
- Clear separation of concerns
- Environment-based configuration
- Better testability by design

**Cons:**
- More upfront complexity
- Requires architectural planning
- Additional dependencies (`dependency-injector`)
- Steeper learning curve
- More boilerplate code

## When to Use Each Approach

### Use Mock-Based Testing when:
- Working with legacy code
- Making quick prototypes
- Testing simple functions
- Your team is already familiar with mocks
- You don't want to change existing architecture

### Use Dependency Injection when:
- Building new applications from scratch
- You need better testability and maintainability
- Your application has complex dependencies
- You want to enforce interfaces and contracts
- You need environment-based configuration
- Your codebase will be maintained long-term

## Key Takeaways

1. **Mock-based testing** is simpler but creates tighter coupling to implementation details
2. **Dependency Injection** requires more setup but provides better long-term maintainability
3. Both approaches are valid; choose based on your project's needs and constraints
4. DI promotes better design patterns (SOLID principles)
5. Mocking is still useful even with DI (for unit testing individual components)

## Technologies Used

- **Python 3.8+**: Programming language
- **requests**: HTTP library for API calls
- **dependency-injector**: DI container framework
- **pytest**: Testing framework
- **unittest.mock**: Python's built-in mocking library

## Further Reading and References

### Official Documentation
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [dependency-injector Documentation](https://python-dependency-injector.ets-labs.org/)
- [pytest Documentation](https://docs.pytest.org/)

### Articles and Guides
- [Dependency Injection in Python](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)
- [SOLID Principles in Python](https://realpython.com/solid-principles-python/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

### Design Patterns
- **Dependency Injection Pattern**: Passing dependencies to objects rather than having them create dependencies
- **Factory Pattern**: Used in `pokemon_service_factory()` to encapsulate object creation
- **Singleton Pattern**: Used for API client to ensure single instance
- **Strategy Pattern**: Different API client implementations that are interchangeable

### Books
- "Clean Code" by Robert C. Martin
- "Test Driven Development: By Example" by Kent Beck
- "Dependency Injection Principles, Practices, and Patterns" by Steven van Deursen and Mark Seemann

## Contributing

Feel free to open issues or submit pull requests with improvements to the examples or documentation.

## License

This project is open source and available for educational purposes.
