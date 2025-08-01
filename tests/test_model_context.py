"""Test context-aware model functions."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from noah123d.model import Model, add_object, add_object_from_stl, list_objects, get_object_count, clear_objects
from noah123d.directories import ThreeD
from noah123d import Archive3mf


def test_model_context_function_with_checks():
    """Test that model functions work without context object names."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive3mf(archive_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("test.model") as model:
                    # Test adding object using context function
                    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
                    triangles = [[0, 1, 2]]
                    
                    obj_id = add_object(vertices, triangles)
                    assert obj_id == 1
                    
                    # Test listing objects using context function
                    objects = list_objects()
                    assert objects == [1]
                    
                    # Test object count using context function
                    count = get_object_count()
                    assert count == 1
                    
                    # Test adding another object
                    obj_id2 = add_object(vertices, triangles, "support")
                    assert obj_id2 == 2
                    
                    # Check updated count
                    count = get_object_count()
                    assert count == 2
                    
                    # Test clearing objects
                    clear_objects()
                    count = get_object_count()
                    assert count == 0


def test_model_context_function_with_checks_vs_instance_methods():
    """Test that context functions produce same results as instance methods."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive3mf(archive_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("test.model") as model:
                    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
                    triangles = [[0, 1, 2]]
                    
                    # Add object using instance method
                    obj_id1 = model.add_object(vertices, triangles)
                    
                    # Add object using context function  
                    obj_id2 = add_object(vertices, triangles)
                    
                    # Both should return consecutive IDs
                    assert obj_id1 == 1
                    assert obj_id2 == 2
                    
                    # Both methods should see the same objects
                    instance_objects = model.list_objects()
                    context_objects = list_objects()
                    assert instance_objects == context_objects == [1, 2]
                    
                    # Both methods should report same count
                    instance_count = model.get_object_count()
                    context_count = get_object_count()
                    assert instance_count == context_count == 2


def test_model_context_function_with_checks_outside_context():
    """Test that context functions raise appropriate errors when used outside context."""
    # Test outside any context
    with pytest.raises(RuntimeError, match="must be called within a context manager"):
        add_object([[0, 0, 0]], [[0]])
    
    with pytest.raises(RuntimeError, match="must be called within a context manager"):
        list_objects()
    
    with pytest.raises(RuntimeError, match="must be called within a context manager"):
        get_object_count()
    
    with pytest.raises(RuntimeError, match="must be called within a context manager"):
        clear_objects()
    
    # Test in directory context but not model context
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive3mf(archive_path, 'w') as archive:
            with ThreeD() as threed:
                # Model functions should not work in directory context without model
                with pytest.raises(RuntimeError, match="must be called within a context manager"):
                    add_object([[0, 0, 0]], [[0]])


@patch('stl.mesh.Mesh.from_file')
def test_add_object_from_stl_context_function_with_check(mock_stl_from_file):
    """Test adding STL objects using context function."""
    # Mock STL mesh data
    mock_mesh = MagicMock()
    mock_mesh.vectors = [
        [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    ]
    mock_stl_from_file.return_value = mock_mesh
    
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        stl_path = Path(temp_dir) / "test.stl"
        stl_path.touch()  # Create empty STL file
        
        with Archive3mf(archive_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("test.model") as model:
                    # Test adding STL using context function
                    obj_id = add_object_from_stl(stl_path)
                    assert obj_id == 1
                    
                    # Verify object was added
                    count = get_object_count()
                    assert count == 1
                    
                    objects = list_objects()
                    assert objects == [1]


def test_complex_model_workflow_with_context_function_with_checks():
    """Test a complex workflow using only context functions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive3mf(archive_path, 'w') as archive:
            with ThreeD() as threed:
                with Model("complex.model") as model:
                    # Build a complex model using only context functions
                    
                    # Add a triangle
                    vertices1 = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
                    triangles1 = [[0, 1, 2]]
                    obj1 = add_object(vertices1, triangles1, "triangle")
                    
                    # Add a square (2 triangles)
                    vertices2 = [[2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0]]
                    triangles2 = [[0, 1, 2], [0, 2, 3]]
                    obj2 = add_object(vertices2, triangles2, "square")
                    
                    # Verify state
                    assert get_object_count() == 2
                    assert list_objects() == [1, 2]
                    
                    # Remove the triangle
                    from noah123d.model import remove_object, get_object
                    removed = remove_object(obj1)
                    assert removed == True
                    
                    # Verify removal
                    assert get_object_count() == 1
                    assert list_objects() == [2]
                    
                    # Verify we can still get the remaining object
                    remaining_obj = get_object(obj2)
                    assert remaining_obj is not None
                    assert remaining_obj['type'] == 'square'
                    assert len(remaining_obj['vertices']) == 4
                    assert len(remaining_obj['triangles']) == 2
