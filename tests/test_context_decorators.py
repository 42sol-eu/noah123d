"""Unit tests for context decorators."""

import pytest
from contextvars import ContextVar
from typing import Optional
from unittest.mock import MagicMock

from noah123d.context_decorators import context_function_with_check, context_function, auto_context_function_with_checks


# Test classes and context variables
class MockClass:
    """Mock class for testing."""
    
    def __init__(self, name: str):
        self.name = name
    
    def test_method(self, arg1: str, arg2: int = 42) -> str:
        """Test method with arguments."""
        return f"{self.name}: {arg1} {arg2}"
    
    def test_function(self, arg1: str, arg2: int = 42) -> str:
        """Test function method."""
        return f"{self.name}: {arg1} {arg2}"
    
    def no_args(self) -> str:
        """Test method with no arguments."""
        return f"{self.name}: no args"
    
    def no_args_function(self) -> str:
        """Test method with no arguments."""
        return f"{self.name}: no args"
    
    def kwargs_method(self, *args, **kwargs) -> tuple:
        """Test method with *args and **kwargs."""
        return (self.name, args, kwargs)
    
    def kwargs_function(self, *args, **kwargs) -> tuple:
        """Test method with *args and **kwargs."""
        return (self.name, args, kwargs)
    
    def outer_function(self) -> str:
        """Test method for nested context."""
        return f"{self.name}: outer result"


class AnotherMockClass:
    """Another mock class for type checking tests."""
    
    def __init__(self, name: str):
        self.name = name
    
    def test_function(self, arg1: str) -> str:
        """Test function method."""
        return f"{self.name}: {arg1}"
    
    def inner_function(self) -> str:
        """Test method for nested context."""
        return f"{self.name}: inner result"
    
    def different_method(self) -> str:
        return f"Different: {self.name}"


# Context variables for testing
test_context: ContextVar[Optional[MockClass]] = ContextVar('test_context', default=None)
another_context: ContextVar[Optional[AnotherMockClass]] = ContextVar('another_context', default=None)


class TestSimpleContext:
    """Test the context_function decorator."""
    
    def test_context_function_basic_functionality(self):
        """Test basic functionality of context_function decorator."""
        
        @context_function(test_context)
        def test_function(arg1: str, arg2: int = 42) -> str:
            """Test function."""
            pass
        
        # Test without context - should raise error
        with pytest.raises(RuntimeError, match="test_function\\(\\) must be called within a context manager"):
            test_function("hello")
        
        # Test with context - should work
        mock_instance = MockClass("test")
        token = test_context.set(mock_instance)
        
        try:
            result = test_function("hello", 123)
            assert result == "test: hello 123"
        finally:
            test_context.reset(token)
    
    def test_context_function_no_args(self):
        """Test context_function with method that takes no arguments."""
        
        @context_function(test_context)
        def no_args_function() -> str:
            pass
        
        mock_instance = MockClass("test")
        token = test_context.set(mock_instance)
        
        try:
            result = no_args_function()
            assert result == "test: no args"
        finally:
            test_context.reset(token)
    
    def test_context_function_with_kwargs(self):
        """Test context_function with *args and **kwargs."""
        
        @context_function(test_context)
        def kwargs_function(*args, **kwargs) -> tuple:
            pass
        
        mock_instance = MockClass("test")
        token = test_context.set(mock_instance)
        
        try:
            result = kwargs_function("arg1", "arg2", key1="value1", key2="value2")
            expected = ("test", ("arg1", "arg2"), {"key1": "value1", "key2": "value2"})
            assert result == expected
        finally:
            test_context.reset(token)
    
    def test_context_function_missing_method(self):
        """Test context_function when method doesn't exist on instance."""
        
        @context_function(test_context)
        def missing_method() -> str:
            pass
        
        mock_instance = MockClass("test")
        token = test_context.set(mock_instance)
        
        try:
            with pytest.raises(AttributeError, match="'MockClass' object has no attribute 'missing_method'"):
                missing_method()
        finally:
            test_context.reset(token)


class TestContextFunction:
    """Test the context_function_with_check decorator."""
    
    def test_context_function_with_check_basic_functionality(self):
        """Test basic functionality of context_function_with_check decorator."""
        
        @context_function_with_check(test_context, MockClass, "MockClass")
        def test_function(arg1: str, arg2: int = 42) -> str:
            pass
        
        # Test without context
        with pytest.raises(RuntimeError, match="test_function\\(\\) must be called within a MockClass context manager"):
            test_function("hello")
        
        # Test with correct context
        mock_instance = MockClass("test")
        token = test_context.set(mock_instance)
        
        try:
            result = test_function("hello", 123)
            assert result == "test: hello 123"
        finally:
            test_context.reset(token)
    
    def test_context_function_with_check_type_checking(self):
        """Test type checking in context_function_with_check decorator."""
        
        @context_function_with_check(test_context, MockClass, "MockClass")
        def test_function() -> str:
            pass
        
        # Test with wrong type
        wrong_instance = AnotherMockClass("wrong")
        token = test_context.set(wrong_instance)
        
        try:
            with pytest.raises(TypeError, match="test_function\\(\\) can only be used within a MockClass context"):
                test_function()
        finally:
            test_context.reset(token)
    
    def test_context_function_with_check_no_type_checking(self):
        """Test context_function_with_check without type checking."""
        
        @context_function_with_check(test_context)
        def test_function(arg1: str) -> str:
            pass
        
        # Should work with any type when no expected_type is provided
        wrong_instance = AnotherMockClass("any")
        
        token = test_context.set(wrong_instance)
        
        try:
            result = test_function("hello")
            assert result == "any: hello"
        finally:
            test_context.reset(token)
    
    def test_context_function_with_check_auto_context_name(self):
        """Test context_function_with_check with auto-derived context name."""
        
        @context_function_with_check(test_context, MockClass)
        def test_function() -> str:
            pass
        
        # Should auto-derive context name from type
        with pytest.raises(RuntimeError, match="test_function\\(\\) must be called within a MockClass context manager"):
            test_function()
    
    def test_context_function_with_check_no_expected_type_fallback(self):
        """Test context_function_with_check fallback when no expected_type."""
        
        @context_function_with_check(test_context)
        def test_function() -> str:
            pass
        
        # Should use "context" as fallback name
        with pytest.raises(RuntimeError, match="test_function\\(\\) must be called within a context context manager"):
            test_function()


class TestAutoContextFunctions:
    """Test the auto_context_function_with_checks utility."""
    
    def test_auto_context_function_with_checks_basic(self):
        """Test basic auto_context_function_with_checks functionality."""
        
        methods = ["test_method", "no_args"]
        functions = auto_context_function_with_checks(
            test_context, 
            MockClass, 
            "MockClass", 
            methods
        )
        
        assert len(functions) == 2
        assert "test_method" in functions
        assert "no_args" in functions
        
        # Test the generated functions
        mock_instance = MockClass("auto")
        token = test_context.set(mock_instance)
        
        try:
            # Test test_method function
            result1 = functions["test_method"]("hello", 99)
            assert result1 == "auto: hello 99"
            
            # Test no_args function
            result2 = functions["no_args"]()
            assert result2 == "auto: no args"
        finally:
            test_context.reset(token)
    
    def test_auto_context_function_with_checks_empty_methods(self):
        """Test auto_context_function_with_checks with empty methods list."""
        
        functions = auto_context_function_with_checks(test_context, MockClass, "MockClass", [])
        assert functions == {}
    
    def test_auto_context_function_with_checks_none_methods(self):
        """Test auto_context_function_with_checks with None methods."""
        
        functions = auto_context_function_with_checks(test_context, MockClass, "MockClass", None)
        assert functions == {}


class TestDecoratorIntegration:
    """Test decorators working together and edge cases."""
    
    def test_nested_contexts(self):
        """Test decorators with nested contexts."""
        
        @context_function(test_context)
        def outer_function() -> str:
            pass
        
        @context_function_with_check(another_context, AnotherMockClass, "AnotherMockClass")
        def inner_function() -> str:
            pass
        
        # Set up nested contexts
        mock1 = MockClass("outer")
        mock2 = AnotherMockClass("inner")
        
        token1 = test_context.set(mock1)
        token2 = another_context.set(mock2)
        
        try:
            result1 = outer_function()
            result2 = inner_function()
            
            assert result1 == "outer: outer result"
            assert result2 == "inner: inner result"
        finally:
            another_context.reset(token2)
            test_context.reset(token1)
    
    def test_function_metadata_preservation(self):
        """Test that decorators preserve function metadata."""
        
        @context_function(test_context)
        def documented_function(arg: str) -> str:
            """This is a test function with documentation."""
            pass
        
        # Check that metadata is preserved
        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a test function with documentation."
        
        # Check annotations are preserved (Python 3.9+)
        if hasattr(documented_function, '__annotations__'):
            assert 'arg' in documented_function.__annotations__
            assert documented_function.__annotations__.get('return') == str
    
    def test_decorator_with_mock_object(self):
        """Test decorators with mock objects."""
        
        @context_function(test_context)
        def mock_function(value: int) -> int:
            pass
        
        # Create a mock that responds to mock_function calls
        mock_instance = MagicMock()
        mock_instance.mock_function.return_value = 42
        
        token = test_context.set(mock_instance)
        
        try:
            result = mock_function(123)
            assert result == 42
            mock_instance.mock_function.assert_called_once_with(123)
        finally:
            test_context.reset(token)


class TestErrorMessages:
    """Test error message formatting and details."""
    
    def test_runtime_error_messages(self):
        """Test RuntimeError message formatting."""
        
        @context_function_with_check(test_context, MockClass, "TestContext")
        def specific_function() -> str:
            pass
        
        with pytest.raises(RuntimeError) as exc_info:
            specific_function()
        
        error_msg = str(exc_info.value)
        assert "specific_function()" in error_msg
        assert "TestContext context manager" in error_msg
    
    def test_type_error_messages(self):
        """Test TypeError message formatting."""
        
        @context_function_with_check(test_context, MockClass, "SpecificType")
        def type_specific_function() -> str:
            pass
        
        wrong_instance = AnotherMockClass("wrong")
        token = test_context.set(wrong_instance)
        
        try:
            with pytest.raises(TypeError) as exc_info:
                type_specific_function()
            
            error_msg = str(exc_info.value)
            assert "type_specific_function()" in error_msg
            assert "SpecificType context" in error_msg
        finally:
            test_context.reset(token)
    
    def test_attribute_error_passthrough(self):
        """Test that AttributeErrors from missing methods are passed through."""
        
        @context_function(test_context)
        def nonexistent_method() -> None:
            pass
        
        mock_instance = MockClass("test")
        token = test_context.set(mock_instance)
        
        try:
            with pytest.raises(AttributeError, match="'MockClass' object has no attribute 'nonexistent_method'"):
                nonexistent_method()
        finally:
            test_context.reset(token)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
