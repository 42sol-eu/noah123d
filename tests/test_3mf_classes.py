"""Test the Archive3mf, Directory, and Model classes."""

import tempfile
import pytest
from pathlib import Path
from noah123d import Archive3mf, Directory, Model


def test_archive_context_manager():
    """Test Archive3mf context manager."""
    with tempfile.NamedTemporaryFile(suffix='.3mf', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    try:
        # Test creating a new archive
        with Archive3mf(tmp_path, 'w') as archive:
            assert archive is not None
            assert Archive3mf.get_current() == archive
            contents = archive.list_contents()
            assert '[Content_Types].xml' in contents
            assert '_rels/.rels' in contents
            
        # Context should be reset after exit
        assert Archive3mf.get_current() is None
        
    finally:
        tmp_path.unlink(missing_ok=True)


def test_directory_context_manager():
    """Test Directory context manager within Archive context."""
    with tempfile.NamedTemporaryFile(suffix='.3mf', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    try:
        with Archive3mf(tmp_path, 'w') as archive:
            with Directory('3D') as directory:
                assert directory is not None
                assert Directory.get_current() == directory
                assert Directory.get_parent_archive() == archive
                
                # Test directory operations
                directory.create_file('test.txt', 'Hello, World!')
                content = directory.read_file('test.txt')
                assert content == b'Hello, World!'
                
        # Context should be reset after exit
        assert Directory.get_current() is None
        
    finally:
        tmp_path.unlink(missing_ok=True)


def test_model_context_manager():
    """Test Model context manager within Archive context."""
    with tempfile.NamedTemporaryFile(suffix='.3mf', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    try:
        with Archive3mf(tmp_path, 'w') as archive:
            with Directory('3D') as directory:
                with Model() as model:
                    assert model is not None
                    assert Model.get_current() == model
                    assert Model.get_parent_archive() == archive
                    
                    # Test adding a simple cube
                    vertices = [
                        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom
                        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # top
                    ]
                    triangles = [
                        [0, 1, 2], [0, 2, 3],  # bottom
                        [4, 7, 6], [4, 6, 5],  # top
                        [0, 4, 5], [0, 5, 1],  # front
                        [2, 6, 7], [2, 7, 3],  # back
                        [0, 3, 7], [0, 7, 4],  # left
                        [1, 5, 6], [1, 6, 2]   # right
                    ]
                    
                    obj_id = model.add_object(vertices, triangles)
                    assert obj_id == 1
                    assert model.get_object_count() == 1
                    
                    # Test retrieving the object
                    obj = model.get_object(obj_id)
                    assert obj is not None
                    assert obj['id'] == obj_id
                    assert len(obj['vertices']) == 8
                    assert len(obj['triangles']) == 12
                    
        # Context should be reset after exit
        assert Model.get_current() is None
        
    finally:
        tmp_path.unlink(missing_ok=True)


def test_nested_contexts():
    """Test all three classes working together in nested contexts."""
    with tempfile.NamedTemporaryFile(suffix='.3mf', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    try:
        with Archive3mf(tmp_path, 'w') as archive:
            # Create main 3D directory
            with Directory('3D') as main_dir:
                # Create a model
                with Model() as model:
                    # Add a simple triangle
                    vertices = [[0, 0, 0], [1, 0, 0], [0.5, 1, 0]]
                    triangles = [[0, 1, 2]]
                    
                    obj_id = model.add_object(vertices, triangles)
                    assert obj_id == 1
                    
                # Create a subdirectory for textures
                with Directory('3D/Textures') as texture_dir:
                    texture_dir.create_file('texture.png', b'fake_png_data')
                    assert 'texture.png' in texture_dir.list_files()
                    
            # Verify archive contents
            contents = archive.list_contents()
            assert any('3dmodel.model' in content for content in contents)
            
    finally:
        tmp_path.unlink(missing_ok=True)


def test_context_isolation():
    """Test that contexts are properly isolated."""
    with tempfile.NamedTemporaryFile(suffix='.3mf', delete=False) as tmp1:
        tmp1_path = Path(tmp1.name)
    with tempfile.NamedTemporaryFile(suffix='.3mf', delete=False) as tmp2:
        tmp2_path = Path(tmp2.name)
    
    try:
        # First archive context
        with Archive3mf(tmp1_path, 'w') as archive1:
            assert Archive3mf.get_current() == archive1
            
            with Directory('3D') as dir1:
                assert Directory.get_current() == dir1
                assert Directory.get_parent_archive() == archive1
                
                # Second archive context (nested)
                with Archive3mf(tmp2_path, 'w') as archive2:
                    assert Archive3mf.get_current() == archive2
                    
                    with Directory('Models') as dir2:
                        assert Directory.get_current() == dir2
                        assert Directory.get_parent_archive() == archive2
                        
                # Back to first context
                assert Archive3mf.get_current() == archive1
                assert Directory.get_current() == dir1
                assert Directory.get_parent_archive() == archive1
                
    finally:
        tmp1_path.unlink(missing_ok=True)
        tmp2_path.unlink(missing_ok=True)
