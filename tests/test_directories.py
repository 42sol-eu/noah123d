"""Test specialized directory classes."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from noah123d.threemf import ThreeD, Metadata, Textures, add_thumbnail, create_model_file
from noah123d import Archive


def test_threed_initialization():
    """Test ThreeD directory initialization."""
    threed = ThreeD()
    assert str(threed.path) == "3D"
    assert threed.create is True
    
    threed_no_create = ThreeD(create=False)
    assert threed_no_create.create is False


def test_threed_create_model_file():
    """Test creating model files in ThreeD directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with ThreeD() as threed:
                # Test valid model file creation
                threed.create_model_file("test.model", "<model>content</model>")
                
                # Test invalid extension should raise error
                with pytest.raises(ValueError, match="Model files should have a .model extension"):
                    threed.create_model_file("test.txt", "content")


def test_threed_add_thumbnail():
    """Test adding thumbnails to ThreeD directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with ThreeD() as threed:
                # Test valid thumbnail formats using context object
                threed.add_thumbnail("thumb.png", b"fake_png_data")
                threed.add_thumbnail("thumb.jpg", b"fake_jpg_data")
                threed.add_thumbnail("thumb.JPEG", b"fake_jpeg_data")
                
                # Test invalid format should raise error
                with pytest.raises(ValueError, match="Thumbnail must be one of"):
                    threed.add_thumbnail("thumb.txt", b"fake_data")


def test_threed_add_thumbnail_context_function_with_checks():
    """Test adding thumbnails using context-aware module functions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with ThreeD() as threed:
                # Test valid thumbnail formats using module functions (no context object needed)
                add_thumbnail("thumb.png", b"fake_png_data")
                add_thumbnail("thumb.jpg", b"fake_jpg_data") 
                add_thumbnail("thumb.JPEG", b"fake_jpeg_data")
                
                # Test invalid format should raise error
                with pytest.raises(ValueError, match="Thumbnail must be one of"):
                    add_thumbnail("thumb.txt", b"fake_data")


def test_threed_create_model_file_context_function_with_checks():
    """Test creating model files using context-aware module functions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with ThreeD() as threed:
                # Test valid model file creation using module function
                create_model_file("test.model", "<model>content</model>")
                
                # Test invalid extension should raise error
                with pytest.raises(ValueError, match="Model files should have a .model extension"):
                    create_model_file("test.txt", "content")


def test_context_function_with_checks_outside_context():
    """Test that context functions raise appropriate errors when used outside context."""
    # Test outside any context
    with pytest.raises(RuntimeError, match="must be called within a ThreeD context manager"):
        add_thumbnail("thumb.png", b"fake_data")
    
    with pytest.raises(RuntimeError, match="must be called within a ThreeD context manager"):
        create_model_file("test.model", "content")
    
    # Test in wrong context type
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Metadata() as metadata:
                # ThreeD functions should not work in Metadata context
                with pytest.raises(TypeError, match="can only be used within a ThreeD context"):
                    add_thumbnail("thumb.png", b"fake_data")
                
                with pytest.raises(TypeError, match="can only be used within a ThreeD context"):
                    create_model_file("test.model", "content")


def test_metadata_initialization():
    """Test Metadata directory initialization."""
    metadata = Metadata()
    assert str(metadata.path) == "Metadata"
    assert metadata.create is True


def test_metadata_add_conversion_info():
    """Test adding conversion info to Metadata directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Metadata() as metadata:
                metadata.add_conversion_info(
                    source_file="test.stl",
                    converter="noah123d",
                    objects_count=5,
                    additional_info={"author": "test"}
                )
                
                # Verify file was created
                files = metadata.list_files()
                assert "conversion_info.txt" in files


def test_metadata_add_properties():
    """Test adding properties to Metadata directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Metadata() as metadata:
                properties = {"material": "PLA", "color": "red"}
                metadata.add_properties(properties)
                
                # Verify file was created
                files = metadata.list_files()
                assert "properties.xml" in files
                
                # Test custom filename
                metadata.add_properties(properties, "custom.xml")
                files = metadata.list_files()
                assert "custom.xml" in files


def test_metadata_add_custom_metadata():
    """Test adding custom metadata."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Metadata() as metadata:
                metadata.add_custom_metadata(
                    "custom.json", 
                    '{"key": "value"}',
                    "Test description"
                )
                
                files = metadata.list_files()
                assert "custom.json" in files
                assert "custom_description.txt" in files


def test_textures_initialization():
    """Test Textures directory initialization."""
    textures = Textures()
    assert str(textures.path) == "Textures"
    assert textures.create is True


def test_textures_add_texture():
    """Test adding textures to Textures directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Textures() as textures:
                # Test valid texture formats
                textures.add_texture("texture.png", b"fake_png", "color")
                textures.add_texture("normal.jpg", b"fake_jpg", "normal")
                
                # Test invalid format should raise error
                with pytest.raises(ValueError, match="Texture must be one of"):
                    textures.add_texture("texture.txt", b"fake_data")
                
                # Verify files were created
                files = textures.list_files()
                assert "texture.png" in files
                assert "texture_metadata.txt" in files
                assert "normal.jpg" in files
                assert "normal_metadata.txt" in files


def test_textures_list_texture_files():
    """Test listing texture files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Textures() as textures:
                textures.add_texture("texture1.png", b"fake_png")
                textures.add_texture("texture2.jpg", b"fake_jpg")
                textures.create_file("metadata.txt", "not a texture")
                
                texture_files = textures.list_texture_files()
                assert "texture1.png" in texture_files
                assert "texture2.jpg" in texture_files
                assert "metadata.txt" not in texture_files


def test_textures_get_texture_metadata():
    """Test getting texture metadata."""
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Textures() as textures:
                textures.add_texture("test.png", b"fake_png", "normal")
                
                metadata = textures.get_texture_metadata("test.png")
                assert metadata is not None
                assert "Texture Type: normal" in metadata
                assert "Filename: test.png" in metadata
                
                # Test non-existent texture
                metadata = textures.get_texture_metadata("nonexistent.png")
                assert metadata is None


def test_backward_compatibility():
    """Test that old Directory class still works alongside new classes."""
    from noah123d import Directory
    # Skip specialized directory import test as the module structure has changed
    assert Directory is not None
    
    # Old usage should still work
    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "test.3mf"
        
        with Archive(archive_path, 'w') as archive:
            with Directory('3D') as old_style:
                old_style.create_file("test.model", "content")
                files = old_style.list_files()
                assert "test.model" in files
