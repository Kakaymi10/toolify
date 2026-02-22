import inspect
import json
import enum
from typing import get_type_hints, Any, Dict, List, Union, Optional, Type, Callable
from pydantic import BaseModel

def toolify(func):
    """
    Decorator to mark a function as a tool.
    In this MVP, it just marks it. 
    Real schema generation happens in get_schema().
    """
    func._is_toolify = True
    return func

def get_schema(func: Callable) -> Dict[str, Any]:
    """
    Generate an OpenAI-compatible JSON schema for a function.
    """
    if not hasattr(func, "_is_toolify"):
        # You can call get_schema on undecorated functions too, 
        # but the decorator is good practice.
        pass

    name = func.__name__
    doc = inspect.getdoc(func)
    description = doc.split("\n\n")[0] if doc else f"Call function {name}"
    
    # 1. Type Hints
    type_hints = get_type_hints(func)
    sig = inspect.signature(func)
    
    properties = {}
    required = []
    
    # 2. Iterate Parameters
    for param_name, param in sig.parameters.items():
        # Skip 'self' or 'cls' if method (simplification)
        if param_name in ("self", "cls"):
            continue
            
        py_type = type_hints.get(param_name, str)
        param_desc = _extract_param_desc(doc, param_name)
        
        # 3. Resolve JSON Schema Type
        prop_schema = _py_type_to_json_schema(py_type)
        if param_desc:
            prop_schema["description"] = param_desc
            
        # 4. Handle Defaults
        if param.default != inspect.Parameter.empty:
            prop_schema["default"] = param.default
        else:
            required.append(param_name)
            
        properties[param_name] = prop_schema

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

def _extract_param_desc(doc: str, param_name: str) -> Optional[str]:
    """
    Simple docstring parser for 'Args:' section.
    Looks for lines like '  param_name (type): Description...'
    """
    if not doc:
        return None
    
    lines = doc.split('\n')
    for line in lines:
        line = line.strip()
        # Very naive parser: looks for "name (type): desc" or "name: desc"
        if line.startswith(f"{param_name}"):
            if ":" in line:
                return line.split(":", 1)[1].strip()
    return None

def _py_type_to_json_schema(py_type: Type) -> Dict[str, Any]:
    """
    Map Python types to JSON schema.
    Supports: str, int, float, bool, list, dict, Enum, Pydantic models.
    """
    # 1. Pydantic Models
    if isinstance(py_type, type) and issubclass(py_type, BaseModel):
        # Pydantic has a built-in schema generator
        schema = py_type.model_json_schema()
        # Remove 'title' to keep it clean if desired, or keep it
        return schema

    # 2. Primitives
    if py_type == str:
        return {"type": "string"}
    if py_type == int:
        return {"type": "integer"}
    if py_type == float:
        return {"type": "number"}
    if py_type == bool:
        return {"type": "boolean"}
    if py_type == list or getattr(py_type, "__origin__", None) == list:
        # TODO: Handle List[int] etc.
        return {"type": "array", "items": {}} 
    if py_type == dict or getattr(py_type, "__origin__", None) == dict:
        return {"type": "object"}
        
    # 3. Enums
    if isinstance(py_type, type) and issubclass(py_type, enum.Enum):
        return {
            "type": "string",
            "enum": [e.value for e in py_type]
        }
        
    # Default fallback
    return {"type": "string"}
