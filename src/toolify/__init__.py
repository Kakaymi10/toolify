import inspect
from typing import get_type_hints

def agent_tool(func):
    """
    Decorator that attaches a .to_schema() method to the function.
    
    Usage:
        @agent_tool
        def my_func(a: int): ...
        
        print(my_func.to_schema())
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null"
    }

    # 1. Get Metadata
    name = func.__name__
    description = func.__doc__.strip() if func.__doc__ else f"Call {name}"
    
    # 2. Analyze Arguments (Type Hints)
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    properties = {}
    required = []

    for param_name, param in sig.parameters.items():
        # Get Python Type
        py_type = type_hints.get(param_name, str) # Default to str if untyped
        
        # Map to JSON Type
        # Handle simple optional types like Optional[int] roughly by checking origins if needed
        # For MVP, we stick to direct mapping
        json_type = type_map.get(py_type, "string")
        
        # Build Property
        properties[param_name] = {
            "type": json_type,
            "description": f"Value for {param_name}" # TODO: Parse from docstring
        }
        
        # Check if required (no default value)
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    # 3. Construct Schema
    schema = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }

    # Attach to function
    func.to_schema = lambda: schema
    return func
