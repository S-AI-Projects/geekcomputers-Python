import importlib.util
from pathlib import Path

import pytest


SOURCE = Path(__file__).resolve().parents[2] / "smart_file_organizer.py"


@pytest.fixture
def organizer_module(monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "smart_file_organizer_test", SOURCE
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    existing_paths = set()
    created_paths = []

    def fake_exists(path):
        return path in existing_paths

    def fake_makedirs(path, exist_ok=False):
        if path in existing_paths:
            if not exist_ok:
                raise FileExistsError(path)
            return

        existing_paths.add(path)
        created_paths.append(path)

    monkeypatch.setattr(module.os.path, "exists", fake_exists)
    monkeypatch.setattr(module.os, "makedirs", fake_makedirs)

    return module, existing_paths, created_paths


def test_create_folder_with_smallest_valid_path(organizer_module):
    module, existing, created = organizer_module

    # Preconditions: smart_file_organizer.py lines 37 and 42.
    folder_path = "a"
    expected_created = ["a"]

    result = module.create_folder(folder_path)

    assert result is None
    assert folder_path in existing
    assert created == expected_created


def test_create_folder_with_ordinary_nested_path(organizer_module):
    module, existing, created = organizer_module

    # Preconditions: smart_file_organizer.py lines 37 and 42.
    folder_path = "reports/2026"
    expected_created = ["reports/2026"]

    result = module.create_folder(folder_path)

    assert result is None
    assert folder_path in existing
    assert created == expected_created


def test_existing_folder_is_not_duplicated(organizer_module):
    module, existing, created = organizer_module

    # Preconditions: smart_file_organizer.py lines 44-45.
    folder_path = "a"
    existing.add(folder_path)

    result = module.create_folder(folder_path)

    assert result is None
    assert folder_path in existing
    assert created == []
