# 🛠️ Toolify

**Stop writing JSON schemas by hand.**

Toolify converts your Python functions into OpenAI/Anthropic/Gemini-compatible tool schemas instantly using a simple decorator.

## Installation

```bash
pip install toolify-ai
```

## Usage

```python
import json
from toolify import agent_tool

@agent_tool
def calculate_vat(amount: float, country_code: str):
    """
    Calculates the Value Added Tax for a given country.
    """
    # Your actual logic here...
    return amount * 0.2

# Generate the schema automatically
print(json.dumps(calculate_vat.to_schema(), indent=2))
```

**Output:**

```json
{
  "name": "calculate_vat",
  "description": "Calculates the Value Added Tax for a given country.",
  "parameters": {
    "type": "object",
    "properties": {
      "amount": { "type": "number", "description": "Value for amount" },
      "country_code": { "type": "string", "description": "Value for country_code" }
    },
    "required": ["amount", "country_code"]
  }
}
```

## Why?

Agent engineering shouldn't mean writing boilerplate JSON. Keep your code and your schemas in sync automatically.
