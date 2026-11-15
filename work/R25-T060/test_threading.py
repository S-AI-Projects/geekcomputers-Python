import importlib.util
from pathlib import Path

import pytest


import os

SOURCE = Path(
    os.environ.get(
        "T060_SOURCE_PATH",
        Path(__file__).resolve().parents[2] / "youtubedownloader.py",
    )
)


@pytest.fixture
def downloader_module(monkeypatch):
    # Import only the named module; prevent GUI and YouTube dependencies.
    import sys
    import types

    tkinter_stub = types.ModuleType("tkinter")
    tkinter_stub.Button = object
    tkinter_stub.Entry = object
    tkinter_stub.Label = object
    tkinter_stub.Tk = object
    tkinter_stub.filedialog = types.SimpleNamespace()
    tkinter_stub.messagebox = types.SimpleNamespace()

    pytube_stub = types.ModuleType("pytube")
    pytube_stub.YouTube = object

    monkeypatch.setitem(sys.modules, "tkinter", tkinter_stub)
    monkeypatch.setitem(sys.modules, "pytube", pytube_stub)

    spec = importlib.util.spec_from_file_location(
        "youtube_downloader_test", SOURCE
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_smallest_call_starts_thread_with_download_target(
    downloader_module, monkeypatch
):
    # Source line 9: Thread must receive download as its target.
    # Source line 10: the created thread must be started.
    created = []

    class FakeThread:
        def __init__(self, *, target):
            self.target = target
            self.start_calls = 0
            created.append(self)

        def start(self):
            self.start_calls += 1

    monkeypatch.setattr(downloader_module, "Thread", FakeThread)

    result = downloader_module.threading()

    assert result is None
    assert len(created) == 1
    assert created[0].target is downloader_module.download
    assert created[0].start_calls == 1


def test_ordinary_repeated_call_creates_fresh_started_thread(
    downloader_module, monkeypatch
):
    # Source lines 9-10: each call creates and starts a worker thread.
    created = []

    class FakeThread:
        def __init__(self, *, target):
            self.target = target
            self.start_calls = 0
            created.append(self)

        def start(self):
            self.start_calls += 1

    monkeypatch.setattr(downloader_module, "Thread", FakeThread)

    first_result = downloader_module.threading()
    second_result = downloader_module.threading()

    assert first_result is None
    assert second_result is None
    assert len(created) == 2
    assert created[0] is not created[1]
    assert created[0].target is downloader_module.download
    assert created[1].target is downloader_module.download
    assert created[0].start_calls == 1
    assert created[1].start_calls == 1
