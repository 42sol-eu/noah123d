"""Decorator utilities for creating context-aware functions."""

from functools import wraps
from typing import Callable, TypeVar, Type, Any, Optional
from contextvars import ContextVar

T = TypeVar('T')


def context_function(context_var: ContextVar[Optional[T]], 
                    expected_type: Type[T] = None,
                    context_name: str = None) -> Callable:
    """Decorator to create context-aware functions that delegate to instance methods.
    
    Args:
        context_var: The ContextVar to get the current instance from
        expected_type: Optional type to check the context instance against
        context_name: Name of the context for error messages (auto-derived if None)
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get current instance from context
            current_instance = context_var.get()
            
            # Check if we have a context
            if not current_instance:
                ctx_name = context_name or (expected_type.__name__ if expected_type else "context")
                raise RuntimeError(f"{func.__name__}() must be called within a {ctx_name} context manager")
            
            # Check type if specified
            if expected_type and not isinstance(current_instance, expected_type):
                ctx_name = context_name or expected_type.__name__
                raise TypeError(f"{func.__name__}() can only be used within a {ctx_name} context")
            
            # Get the method name (same as function name by default)
            method_name = func.__name__
            
            # Get the method from the instance
            if not hasattr(current_instance, method_name):
                raise AttributeError(f"{type(current_instance).__name__} has no method '{method_name}'")
            
            method = getattr(current_instance, method_name)
            
            # Call the method with the provided arguments
            return method(*args, **kwargs)
        
        return wrapper
    return decorator


def auto_context_functions (context_var: ContextVar[Optional[T]], 
                            expected_type: Type[T] = None,
                            context_name: str = None,
                            methods: list[str] = None) -> dict[str, Callable]:
    """Automatically create context functions for a list of method names.
    
    Args:
        context_var: The ContextVar to get the current instance from
        expected_type: Optional type to check the context instance against
        context_name: Name of the context for error messages
        methods: List of method names to create context functions for
    
    Returns:
        Dictionary of function_name -> context_function
    """
    functions = {}
    
    for method_name in (methods or []):
        # Create a dummy function with the right name and signature
        def make_context_func(name: str):
            def context_func(*args, **kwargs):
                pass
            context_func.__name__ = name
            context_func.__qualname__ = name
            return context_func
        
        # Apply the decorator
        context_func = context_function(context_var, expected_type, context_name)(
            make_context_func(method_name)
        )
        
        functions[method_name] = context_func
    
    return functions


# Alternative simpler decorator for single-type contexts
def simple_context(context_var: ContextVar) -> Callable:
    """Simple decorator for context functions - no type checking.
    
    Args:
        context_var: The ContextVar to get the current instance from
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_instance = context_var.get()
            if not current_instance:
                raise RuntimeError(f"{func.__name__}() must be called within a context manager")
            
            method = getattr(current_instance, func.__name__)
            return method(*args, **kwargs)
        
        return wrapper
    return decorator
