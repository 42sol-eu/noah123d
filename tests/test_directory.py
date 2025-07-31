"""Test model class.
- state: open, 2025-07-31
"""

import pytest
from unittest.mock import MagicMock, patch
from noah123d import Model, Directory
from pathlib import Path

@pytest.fixture
def a_model():
    return Model("test.model")

@pytest.fixture
def a_directory():
    return Directory("test_directory")

@pytest.fixture
def mock_archive(tmp_path):
    mock = MagicMock()
    mock.get_temp_path.return_value = tmp_path
    return mock

def test_directory_context_sets_and_resets_current_directory(mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        dir_path = "dir1"
        d = Directory(dir_path)
        with d:
            assert Directory.get_current() is d
        assert Directory.get_current() is None

def test_ensure_directory_exists_creates_directory(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir2")
        with d:
            full_path = tmp_path / "dir2"
            assert full_path.exists()
            assert full_path.is_dir()

def test_create_and_read_file(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir3")
        with d:
            d.create_file("file.txt", "hello world")
            files = d.list_files()
            assert "file.txt" in files
            content = d.read_file("file.txt")
            assert content == b"hello world"

def test_create_file_with_bytes(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir4")
        with d:
            d.create_file("file.bin", b"\x01\x02")
            content = d.read_file("file.bin")
            assert content == b"\x01\x02"

def test_delete_file(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir5")
        with d:
            d.create_file("file.txt", "data")
            assert d.delete_file("file.txt") is True
            assert d.read_file("file.txt") is None
            assert d.delete_file("file.txt") is False

def test_list_subdirectories(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir6")
        with d:
            subdir = d.create_subdirectory("sub1")
            with patch.object(subdir, "_parent_archive", mock_archive):
                subdir._ensure_directory_exists()
            subdirs = d.list_subdirectories()
            assert "sub1" in subdirs

def test_get_archive_path_slash_conversion():
    d = Directory("foo\\bar\\baz")
    assert d.get_archive_path() == "foo/bar/baz"

def test_exists_returns_true_when_directory_exists(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir7")
        with d:
            assert d.exists() is True

def test_exists_returns_false_when_directory_does_not_exist(tmp_path, mock_archive):
    with patch("noah123d.directory.current_archive") as mock_current_archive:
        mock_current_archive.get.return_value = mock_archive
        d = Directory("dir8")
        # Do not enter context, so directory is not created
        assert d.exists() is False

def test_get_full_path_returns_none_without_archive():
    d = Directory("dir9")
    assert d.get_full_path() is None

def test_context_raises_if_no_archive():
    d = Directory("dir10")
    with pytest.raises(RuntimeError):
        with d:
            pass

