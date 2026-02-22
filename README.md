# Toolify-AI: The Standard for Agentic Tools

[![PyPI version](https://badge.fury.io/py/toolify-ai.svg)](https://badge.fury.io/py/toolify-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Stop writing JSON boilerplate for your AI agents.**

`toolify-ai` is a lightweight, dependency-free Python library that automatically generates OpenAI-compatible tool schemas from your Python functions and classes. It handles type hints, docstrings, and complex types so you can focus on building agents, not wrestling with JSON.

## Why Toolify?

-   **Zero Boilerplate:** Define your tools as Python functions with type hints and docstrings. Toolify does the rest.
-   **Type-Safe:** Full support for standard Python types (`str`, `int`, `bool`, `float`, `list`, `dict`) and Pydantic models.
-   **Universal:** Generates schemas compatible with OpenAI, Anthropic, and other function-calling LLMs.
-   **Lightweight:** No heavy dependencies. Just install and go.

## Installation

```bash
pip install toolify-ai
```

## Quick Start

### 1. Define Your Function

Just write a standard Python function with type hints and a docstring.

```python
from toolify import toolify

@toolify
def get_weather(location: str, unit: str = "celsius") -> dict:
    """
    Get the current weather for a given location.

    Args:
        location (str): The city and state, e.g. San Francisco, CA.
        unit (str): The temperature unit to use ('celsius' or 'fahrenheit').
    """
    # ... implementation ...
    pass
```

### 2. Generate the Schema

Toolify automatically converts it to the JSON schema expected by the LLM.

```python
import json
from toolify import get_schema

schema = get_schema(get_weather)
print(json.dumps(schema, indent=2))
```

**Output:**

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather for a given location.",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA."
        },
        "unit": {
          "type": "string",
          "description": "The temperature unit to use ('celsius' or 'fahrenheit').",
          "enum": ["celsius", "fahrenheit"],
          "default": "celsius"
        }
      },
      "required": ["location"]
    }
  }
}
```

## Advanced Usage

### Pydantic Models

Toolify seamlessly integrates with Pydantic for complex data structures.

```python
from pydantic import BaseModel, Field
from toolify import toolify

class SearchQuery(BaseModel):
    query: str = Field(..., description="The search query")
    limit: int = Field(10, description="Max number of results")

@toolify
def search_web(params: SearchQuery):
    """Search the web for information."""
    pass
```

## Contributing

We welcome contributions! Please check out our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License. See [LICENSE](LICENSE) for more information.
