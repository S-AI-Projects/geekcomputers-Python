"""Focused repeatable tests for voice in voice.py with mocked external dependencies.

Precondition citations:
    - Source Line 2: `from gtts import gTTS` TTS engine dependency
    - Source Line 7: `text = "Hello! This is a sample text to convert to speech."`
    - Source Line 12: `tts = gTTS(text=text, lang="en")`
    - Source Line 15: `tts.save("output.mp3")`
    - Source Line 18: `os.system("start output.mp3")`
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import voice


class MockTTSInstance:
    """Mock TTS instance that records save destinations without making network requests."""

    def __init__(self, text, lang):
        self.text = text
        self.lang = lang
        self.saved_to = None

    def save(self, filepath):
        self.saved_to = filepath


class MockTTSFactory:
    """Mock TTS builder factory tracking instance creations."""

    def __init__(self):
        self.instances = []

    def __call__(self, text, lang):
        inst = MockTTSInstance(text, lang)
        self.instances.append(inst)
        return inst


class MockSystemExecutor:
    """Mock system command executor recording invocation strings."""

    def __init__(self):
        self.commands = []

    def __call__(self, cmd):
        self.commands.append(cmd)
        return 0


class TestVoiceRepeatability:
    """Tests repeatability, input isolation, and dependency injection for voice.py."""

    def test_smallest_valid_input(self):
        """Smallest valid input: single-character string 'a'.

        Preconditions:
            - Source line 12: gTTS(text='a', lang='en')
            - Source line 15: tts.save('min.mp3')
            - Source line 18: os.system('start min.mp3')
        Literal input:
            text='a', lang='en', output_file='min.mp3', play=False
        Independently calculated expected output:
            {'text': 'a', 'lang': 'en', 'output_file': 'min.mp3', 'played': False, 'success': True}
        """
        factory = MockTTSFactory()
        executor = MockSystemExecutor()

        res = voice.voice(
            text="a",
            lang="en",
            output_file="min.mp3",
            play=False,
            tts_builder=factory,
            system_executor=executor,
        )

        assert res["success"] is True
        assert res["text"] == "a"
        assert res["output_file"] == "min.mp3"
        assert res["played"] is False
        assert len(factory.instances) == 1
        assert factory.instances[0].saved_to == "min.mp3"
        assert len(executor.commands) == 0

    def test_ordinary_input_with_playback(self):
        """Ordinary input: baseline sentence with mock playback.

        Preconditions:
            - Source line 7: 'Hello! This is a sample text to convert to speech.'
            - Source line 12: lang='en'
            - Source line 18: 'start output.mp3'
        Literal input:
            text='Hello! This is a sample text to convert to speech.'
        Independently calculated expected output:
            Receipt with played=True, command 'start output.mp3' recorded.
        """
        factory = MockTTSFactory()
        executor = MockSystemExecutor()

        res = voice.voice(
            text="Hello! This is a sample text to convert to speech.",
            lang="en",
            output_file="output.mp3",
            play=True,
            tts_builder=factory,
            system_executor=executor,
        )

        assert res["success"] is True
        assert res["text"] == "Hello! This is a sample text to convert to speech."
        assert res["played"] is True
        assert executor.commands == ["start output.mp3"]

    def test_repeatable_invocations_and_isolation(self):
        """Verifies repeated calls remain completely isolated without cross-call state mutation."""
        factory = MockTTSFactory()
        executor = MockSystemExecutor()

        for i in range(5):
            res = voice.voice(
                text=f"Iteration {i}",
                lang="en",
                output_file=f"file_{i}.mp3",
                play=True,
                tts_builder=factory,
                system_executor=executor,
            )
            assert res["success"] is True
            assert res["text"] == f"Iteration {i}"

        assert len(factory.instances) == 5
        assert len(executor.commands) == 5

    def test_failure_handling_isolation(self):
        """Ensures exceptions from TTS generator are gracefully handled and return failure receipt."""
        def broken_factory(text, lang):
            raise IOError("Simulated network timeout")

        res = voice.voice(text="fail", tts_builder=broken_factory)
        assert res["success"] is False
        assert "Simulated network timeout" in res["error"]
