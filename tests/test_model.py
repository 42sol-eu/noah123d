"""Test model class.
- state: passing, 2025-07-31
"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from noah123d import Model

@pytest.fixture
def a_model():
    return Model("test.model")

def test_model_initialization(a_model):
    assert a_model.name == "test.model"
    assert a_model.get_object_count() == 0
    assert a_model.list_objects() == []

def test_add_object(a_model):
    vertices = [[0,0,0], [1,0,0], [0,1,0]]
    triangles = [[0,1,2]]
    obj_id = a_model.add_object(vertices, triangles)
    assert obj_id == 1
    assert a_model.get_object_count() == 1
    obj = a_model.get_object(obj_id)
    assert obj is not None
    assert obj['vertices'] == vertices
    assert obj['triangles'] == triangles

def test_remove_object(a_model):
    vertices = [[0,0,0], [1,0,0], [0,1,0]]
    triangles = [[0,1,2]]
    obj_id = a_model.add_object(vertices, triangles)
    assert a_model.remove_object(obj_id) is True
    assert a_model.get_object_count() == 0
    assert a_model.get_object(obj_id) is None

def test_remove_object_not_found(a_model):
    assert a_model.remove_object(999) is False

def test_clear_objects(a_model):
    a_model.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    a_model.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    a_model.clear_objects()
    assert a_model.get_object_count() == 0
    assert a_model.list_objects() == []

def test_list_objects(a_model):
    ids = [a_model.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]]) for _ in range(3)]
    assert a_model.list_objects() == ids

def test_get_object_not_found(a_model):
    assert a_model.get_object(12345) is None

def test_create_simple_cube():
    cube = Model.create_simple_cube(2.0)
    assert isinstance(cube, Model)
    assert cube.get_object_count() == 1
    obj = cube.get_object(1)
    assert obj is not None
    assert len(obj['vertices']) == 8
    assert len(obj['triangles']) == 12

def test_next_object_id_increments(a_model):
    id1 = a_model.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    id2 = a_model.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    assert id2 == id1 + 1

def test_add_object_from_stl_calls_mesh(monkeypatch, a_model, tmp_path):
    fake_mesh = MagicMock()
    fake_mesh.vectors = [
        [[0,0,0],[1,0,0],[0,1,0]],
        [[1,0,0],[1,1,0],[0,1,0]]
    ]
    monkeypatch.setattr("stl.mesh.Mesh.from_file", lambda path: fake_mesh)
    stl_path = tmp_path / "fake.stl"
    stl_path.write_text("fake stl content")
    obj_id = a_model.add_object_from_stl(stl_path)
    assert obj_id == 1
    obj = a_model.get_object(obj_id)
    assert obj is not None
    assert len(obj['vertices']) == 4
    assert len(obj['triangles']) == 2

def test_save_and_load_model(monkeypatch):
    # Patch Archive3mf and Directory context
    mock_archive = MagicMock()
    mock_archive.extract_file.return_value = None
    mock_archive.is_writable.return_value = True
    mock_archive.add_file = MagicMock()
    mock_directory = MagicMock()
    mock_directory.name = "3D"
    
    # Create mock context variables
    mock_current_archive = MagicMock()
    mock_current_archive.get.return_value = mock_archive
    mock_current_directory = MagicMock() 
    mock_current_directory.get.return_value = mock_directory
    
    # Replace the entire context variables
    monkeypatch.setattr("noah123d.model.current_archive", mock_current_archive)
    monkeypatch.setattr("noah123d.model.current_directory", mock_current_directory)
    
    with Model("test.model") as m:
        m.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    # Should call add_file to save
    assert mock_archive.add_file.called

def test_get_current_and_parent(monkeypatch):
    mock_archive = MagicMock()
    mock_directory = MagicMock()
    
    # Create mock context variables
    mock_current_archive = MagicMock()
    mock_current_archive.get.return_value = mock_archive
    mock_current_directory = MagicMock()
    mock_current_directory.get.return_value = mock_directory
    mock_current_model = MagicMock()
    mock_current_model.get.return_value = None
    
    # Replace the entire context variables
    monkeypatch.setattr("noah123d.model.current_archive", mock_current_archive)
    monkeypatch.setattr("noah123d.model.current_directory", mock_current_directory)
    monkeypatch.setattr("noah123d.model.current_model", mock_current_model)
    
    assert Model.get_parent_archive() == mock_archive
    assert Model.get_parent_directory() == mock_directory
    assert Model.get_current() is None

def test_load_stl_with_info(monkeypatch, a_model, tmp_path, capsys):
    """Test load_stl_with_info method with console output."""
    # Create a fake STL file
    stl_path = tmp_path / "test.stl"
    stl_path.write_text("fake stl content")
    
    # Mock the STL mesh
    fake_mesh = MagicMock()
    fake_mesh.vectors = [
        [[0,0,0],[1,0,0],[0,1,0]],
        [[1,0,0],[1,1,0],[0,1,0]]
    ]
    monkeypatch.setattr("stl.mesh.Mesh.from_file", lambda path: fake_mesh)
    
    # Test successful loading
    obj_id = a_model.load_stl_with_info(stl_path)
    assert obj_id == 1
    
    # Check that object was added
    obj = a_model.get_object(obj_id)
    assert obj is not None
    assert len(obj['vertices']) == 4
    assert len(obj['triangles']) == 2
    
    # Test file not found
    non_existent = tmp_path / "nonexistent.stl"
    result = a_model.load_stl_with_info(non_existent)
    assert result is None

def test_analyze_model_content(a_model, capsys):
    """Test analyze_model_content method."""
    # Test with empty model
    a_model.analyze_model_content()
    captured = capsys.readouterr()
    assert "Model Analysis:" in captured.out
    assert "Total Objects: 0" in captured.out
    
    # Add some objects and test again
    a_model.add_object([[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    a_model.add_object([[0,0,0],[2,0,0],[0,2,0],[2,2,0]], [[0,1,2],[1,2,3]])
    
    a_model.analyze_model_content()
    captured = capsys.readouterr()
    assert "Total Objects: 2" in captured.out
    assert "3D Objects Details" in captured.out

@patch('noah123d.model.Directory')
def test_add_conversion_metadata(mock_directory_class, monkeypatch, a_model, tmp_path, capsys):
    """Test add_conversion_metadata method."""
    stl_path = tmp_path / "test.stl"
    stl_path.write_text("fake stl content")
    
    # Mock archive and directory contexts
    mock_archive = MagicMock()
    mock_directory = MagicMock()
    mock_directory.create_file = MagicMock()
    mock_directory.__enter__ = MagicMock(return_value=mock_directory)
    mock_directory.__exit__ = MagicMock(return_value=None)
    mock_directory_class.return_value = mock_directory
    
    mock_current_archive = MagicMock()
    mock_current_archive.get.return_value = mock_archive
    
    monkeypatch.setattr("noah123d.model.current_archive", mock_current_archive)
    
    # Test with valid archive context
    a_model.add_conversion_metadata(stl_path)
    captured = capsys.readouterr()
    assert "Added conversion metadata" in captured.out
    
    # Test with no archive context
    mock_current_archive.get.return_value = None
    a_model.add_conversion_metadata(stl_path)
    captured = capsys.readouterr()
    assert "No archive context available" in captured.out

@patch('noah123d.model.Archive3mf')
@patch('noah123d.model.Directory')
def test_convert_stl_to_3mf(mock_directory_class, mock_archive_class, monkeypatch, tmp_path, capsys):
    """Test convert_stl_to_3mf class method."""
    stl_path = tmp_path / "test.stl"
    stl_path.write_text("fake stl content")
    output_path = tmp_path / "output.3mf"
    
    # Mock STL mesh
    fake_mesh = MagicMock()
    fake_mesh.vectors = [[[0,0,0],[1,0,0],[0,1,0]]]
    monkeypatch.setattr("stl.mesh.Mesh.from_file", lambda path: fake_mesh)
    
    # Mock archive and directory context managers
    mock_archive = MagicMock()
    mock_archive.file_path = output_path
    mock_archive.extract_file.return_value = None  # No existing model data
    mock_archive.is_writable.return_value = True
    mock_archive.add_file = MagicMock()
    mock_archive.__enter__ = MagicMock(return_value=mock_archive)
    mock_archive.__exit__ = MagicMock(return_value=None)
    mock_archive_class.return_value = mock_archive
    
    mock_directory = MagicMock()
    mock_directory.name = "3D"
    mock_directory.create_file = MagicMock()
    mock_directory.__enter__ = MagicMock(return_value=mock_directory)
    mock_directory.__exit__ = MagicMock(return_value=None)
    mock_directory_class.return_value = mock_directory
    
    # Mock context variables to return the mocked objects
    mock_current_archive = MagicMock()
    mock_current_archive.get.return_value = mock_archive
    mock_current_directory = MagicMock()
    mock_current_directory.get.return_value = mock_directory
    mock_current_model = MagicMock()
    mock_current_model.set.return_value = MagicMock()
    mock_current_model.reset = MagicMock()
    
    monkeypatch.setattr("noah123d.model.current_archive", mock_current_archive)
    monkeypatch.setattr("noah123d.model.current_directory", mock_current_directory)
    monkeypatch.setattr("noah123d.model.current_model", mock_current_model)
    
    # Test successful conversion
    result = Model.convert_stl_to_3mf(stl_path, output_path)
    assert result == output_path
    captured = capsys.readouterr()
    assert "Converting STL to 3MF..." in captured.out
    assert "Conversion completed successfully!" in captured.out
    
    # Test file not found
    non_existent = tmp_path / "nonexistent.stl"
    result = Model.convert_stl_to_3mf(non_existent, output_path)
    assert result is None
    captured = capsys.readouterr()
    assert "STL file not found" in captured.out

@patch('noah123d.model.Archive3mf')
@patch('noah123d.model.Directory')
def test_analyze_3mf_content(mock_directory_class, mock_archive_class, monkeypatch, tmp_path, capsys):
    """Test analyze_3mf_content class method."""
    file_path = tmp_path / "test.3mf"
    file_path.write_text("fake 3mf content")
    
    # Mock archive and directory context managers
    mock_archive = MagicMock()
    mock_archive.list_contents.return_value = ["3D/model.model", "Metadata/info.txt"]
    mock_archive.extract_file.return_value = None  # No existing model data
    mock_archive.__enter__ = MagicMock(return_value=mock_archive)
    mock_archive.__exit__ = MagicMock(return_value=None)
    mock_archive_class.return_value = mock_archive
    
    mock_directory = MagicMock()
    mock_directory.name = "3D"
    mock_directory.__enter__ = MagicMock(return_value=mock_directory)
    mock_directory.__exit__ = MagicMock(return_value=None)
    mock_directory_class.return_value = mock_directory
    
    # Mock context variables to return the mocked objects
    mock_current_archive = MagicMock()
    mock_current_archive.get.return_value = mock_archive
    mock_current_directory = MagicMock()
    mock_current_directory.get.return_value = mock_directory
    mock_current_model = MagicMock()
    mock_current_model.set.return_value = MagicMock()
    mock_current_model.reset = MagicMock()
    
    monkeypatch.setattr("noah123d.model.current_archive", mock_current_archive)
    monkeypatch.setattr("noah123d.model.current_directory", mock_current_directory)
    monkeypatch.setattr("noah123d.model.current_model", mock_current_model)
    
    # Test successful analysis
    Model.analyze_3mf_content(file_path)
    captured = capsys.readouterr()
    assert "Analyzing 3MF file" in captured.out
    assert "Archive Contents" in captured.out
    
    # Test file not found
    non_existent = tmp_path / "nonexistent.3mf"
    Model.analyze_3mf_content(non_existent)
    captured = capsys.readouterr()
    assert "3MF file not found" in captured.out

@patch('noah123d.model.Model.convert_stl_to_3mf')
def test_batch_convert_stl_files(mock_convert, tmp_path, capsys):
    """Test batch_convert_stl_files class method."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    
    # Create test STL files
    stl1 = input_dir / "model1.stl"
    stl2 = input_dir / "model2.stl"
    stl1.write_text("fake stl 1")
    stl2.write_text("fake stl 2")
    
    # Create subdirectory with STL
    sub_dir = input_dir / "subdir"
    sub_dir.mkdir()
    stl3 = sub_dir / "model3.stl"
    stl3.write_text("fake stl 3")
    
    # Mock successful conversions
    mock_convert.side_effect = [
        output_dir / "model1.3mf",
        output_dir / "model2.3mf", 
        output_dir / "model3.3mf"
    ]
    
    # Test successful batch conversion
    result = Model.batch_convert_stl_files(input_dir, output_dir)
    assert len(result) == 3
    assert mock_convert.call_count == 3
    captured = capsys.readouterr()
    assert "Batch converting 3 STL files..." in captured.out
    assert "Batch conversion completed!" in captured.out
    
    # Test directory not found
    non_existent = tmp_path / "nonexistent"
    result = Model.batch_convert_stl_files(non_existent, output_dir)
    assert result == []
    captured = capsys.readouterr()
    assert "Input directory not found" in captured.out
    
    # Test no STL files
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    result = Model.batch_convert_stl_files(empty_dir, output_dir)
    assert result == []
    captured = capsys.readouterr()
    assert "No STL files found" in captured.out