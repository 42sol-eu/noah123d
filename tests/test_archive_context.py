"""Test context-aware Archive3mf functions."""

import pytest
import tempfile
from pathlib import Path

from noah123d.archive3mf import Archive3mf, list_contents, extract_file, add_file, get_temp_path, is_writable


def test_archive_context_functions():
    """Test that archive functions work without context object names."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        # Test write mode
        with Archive3mf(archive_path, 'w') as archive:
            # Test is_writable using context function
            assert is_writable() == True
            
            # Test add_file using context function
            add_file("test.txt", "test content")
            add_file("binary.bin", b"binary data")
            
            # Test list_contents using context function
            contents = list_contents()
            assert "test.txt" in contents
            assert "binary.bin" in contents
            assert "[Content_Types].xml" in contents
            assert "_rels/.rels" in contents
            
            # Test get_temp_path using context function
            temp_path = get_temp_path()
            assert temp_path is not None
            assert temp_path.exists()
            
            # Test extract_file in write mode (should work)
            content = extract_file("test.txt")
            assert content == b"test content"


def test_archive_context_functions_vs_instance_methods():
    """Test that context functions produce same results as instance methods."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive3mf(archive_path, 'w') as archive:
            # Add file using instance method
            archive.add_file("instance.txt", "instance content")
            
            # Add file using context function
            add_file("context.txt", "context content")
            
            # Both methods should see the same contents
            instance_contents = archive.list_contents()
            context_contents = list_contents()
            assert set(instance_contents) == set(context_contents)
            assert "instance.txt" in context_contents
            assert "context.txt" in context_contents
            
            # Both methods should report same writability
            instance_writable = archive.is_writable()
            context_writable = is_writable()
            assert instance_writable == context_writable == True
            
            # Both methods should return same temp path
            instance_temp = archive.get_temp_path()
            context_temp = get_temp_path()
            assert instance_temp == context_temp


def test_archive_context_functions_outside_context():
    """Test that context functions raise appropriate errors when used outside context."""
    # Test outside any context
    with pytest.raises(RuntimeError, match="must be called within an Archive3mf context manager"):
        list_contents()
    
    with pytest.raises(RuntimeError, match="must be called within an Archive3mf context manager"):
        extract_file("test.txt")
    
    with pytest.raises(RuntimeError, match="must be called within an Archive3mf context manager"):
        add_file("test.txt", "content")
    
    with pytest.raises(RuntimeError, match="must be called within an Archive3mf context manager"):
        get_temp_path()
    
    with pytest.raises(RuntimeError, match="must be called within an Archive3mf context manager"):
        is_writable()


def test_archive_context_functions_read_write_modes():
    """Test context functions work correctly in different archive modes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        # Create archive in write mode
        with Archive3mf(archive_path, 'w') as archive:
            assert is_writable() == True
            add_file("data.txt", "initial data")
            initial_contents = list_contents()
        
        # Open in read mode
        with Archive3mf(archive_path, 'r') as archive:
            assert is_writable() == False
            
            # Should be able to read
            content = extract_file("data.txt")
            assert content == b"initial data"
            
            read_contents = list_contents()
            assert set(read_contents) == set(initial_contents)
        
        # Open in append mode (if supported)
        with Archive3mf(archive_path, 'a') as archive:
            assert is_writable() == True
            
            # Should be able to read existing
            content = extract_file("data.txt")
            assert content == b"initial data"
            
            # Should be able to add new
            add_file("new.txt", "new data")
            
            updated_contents = list_contents()
            assert "data.txt" in updated_contents
            assert "new.txt" in updated_contents


def test_complex_archive_workflow_with_context_functions():
    """Test a complex workflow using only context functions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "complex.3mf"
        
        with Archive3mf(archive_path, 'w') as archive:
            # Build archive using only context functions
            
            # Check initial state
            assert is_writable() == True
            initial_contents = list_contents()
            assert len(initial_contents) >= 2  # Should have basic structure
            
            # Add various files
            add_file("text/readme.txt", "This is a readme file")
            add_file("data/values.json", '{"version": "1.0", "objects": 3}')
            add_file("binary/data.bin", b'\x00\x01\x02\x03\x04')
            
            # Check updated contents
            final_contents = list_contents()
            assert "text/readme.txt" in final_contents
            assert "data/values.json" in final_contents
            assert "binary/data.bin" in final_contents
            assert len(final_contents) == len(initial_contents) + 3
            
            # Verify temp path is available
            temp_path = get_temp_path()
            assert temp_path is not None
            assert temp_path.exists()
        
        # Verify archive was created correctly
        with Archive3mf(archive_path, 'r') as archive:
            assert is_writable() == False
            
            # Extract and verify all files
            readme = extract_file("text/readme.txt")
            assert readme == b"This is a readme file"
            
            json_data = extract_file("data/values.json")
            assert json_data == b'{"version": "1.0", "objects": 3}'
            
            binary_data = extract_file("binary/data.bin")
            assert binary_data == b'\x00\x01\x02\x03\x04'
            
            # Verify final contents
            contents = list_contents()
            assert "text/readme.txt" in contents
            assert "data/values.json" in contents
            assert "binary/data.bin" in contents
