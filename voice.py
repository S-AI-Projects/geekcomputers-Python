# modules for use of voice
import os

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

try:
    from colorama import Fore
except ImportError:
    class Fore:
        RED = ""
        RESET = ""


def voice(
    text="Hello! This is a sample text to convert to speech.",
    lang="en",
    output_file="output.mp3",
    play=True,
    tts_builder=None,
    system_executor=None,
):
    """Converts input text to speech and saves to an MP3 file with optional playback.

    Contract & Preconditions (from voice.py baseline):
        - Source line 2: TTS generator dependency (`gTTS`).
        - Source line 7: `text = "Hello! This is a sample text to convert to speech."`.
        - Source line 12: `tts = gTTS(text=text, lang="en")` object creation.
        - Source line 15: `tts.save("output.mp3")` saving the MP3.
        - Source line 18: `os.system("start output.mp3")` media playback command.

    Args:
        text (str): Input text to synthesize.
        lang (str): Language code (default 'en').
        output_file (str): Destination audio path.
        play (bool): Whether to invoke media player.
        tts_builder: Injected TTS factory (defaults to gTTS).
        system_executor: Injected command executor (defaults to os.system).

    Returns:
        dict: Execution receipt containing text, lang, output_file, played status, and success.
    """
    builder = tts_builder if tts_builder is not None else gTTS
    executor = system_executor if system_executor is not None else os.system

    try:
        if builder is None:
            raise RuntimeError("TTS engine not available")
        tts = builder(text=text, lang=lang)
        tts.save(output_file)

        played = False
        if play and executor is not None:
            executor(f"start {output_file}")
            played = True

        return {
            "text": text,
            "lang": lang,
            "output_file": output_file,
            "played": played,
            "success": True,
        }
    except Exception as e:
        print(Fore.RED, e, Fore.RESET)
        return {
            "text": text,
            "lang": lang,
            "output_file": output_file,
            "played": False,
            "success": False,
            "error": str(e),
        }


def main():
    text = "Hello! This is a sample text to convert to speech."
    voice(text=text, lang="en", output_file="output.mp3", play=True)


if __name__ == "__main__":
    main()
