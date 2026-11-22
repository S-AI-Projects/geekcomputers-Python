"""Focused refactoring and contract regression tests for transcript_generator in Audio_Summarizer.py.

Precondition citations:
    - Line 9: `model = whisper.load_model("base")` model initialization.
    - Line 12: `result = model.transcribe("audio.mp4")` transcription execution.
    - Line 15: `provide_summarizer(result)` handoff to summarization step.
"""

import sys
import unittest
from unittest.mock import MagicMock
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import Audio_Summarizer as audio_sum


class TestAudioSummarizerRefactoring(unittest.TestCase):
    """Tests verifying extracted transcribe_audio helper and transcript_generator coordination."""

    def test_smallest_valid_input_empty_transcript(self):
        """Smallest valid input: audio yielding empty transcript text.
        
        Preconditions:
            - Line 12: model.transcribe returns dict with text key
            - Line 15: summarizer receives transcript dict
        Literal input:
            audio_path = "empty.mp4", model returning {"text": ""}
        Independently calculated expected output:
            {"text": ""}
        """
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": ""}
        received_summaries = []

        result = audio_sum.transcript_generator(
            audio_path="empty.mp4",
            model=mock_model,
            summarizer=received_summaries.append
        )

        mock_model.transcribe.assert_called_once_with("empty.mp4")
        self.assertEqual(result, {"text": ""})
        self.assertEqual(received_summaries, [{"text": ""}])

    def test_ordinary_input_transcription(self):
        """Ordinary input: standard transcription result.
        
        Preconditions:
            - Line 9: model_name 'base'
            - Line 12: audio.mp4
            - Line 15: summarizer callback receives result
        Literal input:
            audio_path = "audio.mp4", model returning {"text": "Hello world audio test."}
        Independently calculated expected output:
            {"text": "Hello world audio test."}
        """
        mock_model = MagicMock()
        expected_dict = {"text": "Hello world audio test."}
        mock_model.transcribe.return_value = expected_dict
        received_summaries = []

        result = audio_sum.transcript_generator(
            audio_path="audio.mp4",
            model=mock_model,
            summarizer=received_summaries.append
        )

        mock_model.transcribe.assert_called_once_with("audio.mp4")
        self.assertEqual(result, expected_dict)
        self.assertEqual(received_summaries, [expected_dict])

    def test_extracted_transcribe_audio_responsibility(self):
        """Verify the isolated transcribe_audio function directly."""
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "Extracted helper test."}

        transcription = audio_sum.transcribe_audio(
            audio_file="clip.mp3",
            model_name="small",
            model=mock_model
        )

        mock_model.transcribe.assert_called_once_with("clip.mp3")
        self.assertEqual(transcription, {"text": "Extracted helper test."})


if __name__ == "__main__":
    unittest.main()
