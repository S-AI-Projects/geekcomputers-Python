import os
import re

try:
    import whisper
except ImportError:
    whisper = None

try:
    import openai
except ImportError:
    openai = None


def transcribe_audio(audio_file="audio.mp4", model_name="base", model=None):
    """
    Extract audio transcription calculation using Whisper model.

    Preconditions:
      - Line 9: `model = whisper.load_model("base")` loads model architecture.
      - Line 12: `result = model.transcribe("audio.mp4")` runs audio transcription.
    Returns:
      - Transcription result dictionary containing at least the 'text' key.
    """
    if model is None:
        if whisper is None:
            raise RuntimeError("whisper library is not installed")
        model = whisper.load_model(model_name)
    return model.transcribe(audio_file)


def transcript_generator(audio_path="audio.mp4", model_name="base", model=None, summarizer=None):
    """
    Generate audio transcription and forward result to summarizer.

    Preconditions:
      - Line 9: Whisper base model loaded.
      - Line 12: audio.mp4 transcribed.
      - Line 15: Transcribed text dictionary passed to summarizer.
    """
    result = transcribe_audio(audio_file=audio_path, model_name=model_name, model=model)
    target_summarizer = summarizer if summarizer is not None else provide_summarizer
    target_summarizer(result)
    return result


def provide_summarizer(Text):
    # Set up Groq OpenAI-compatible API credentials
    if openai is None:
        raise RuntimeError("openai library is not installed")

    openai.api_key = os.getenv(
        "OPENAI_API_KEY", "your-api-key-here"
    )  # Replace or set in environment
    openai.api_base = "https://api.groq.com/openai/v1"

    # Extract text from the Whisper result
    text_to_summarize = Text["text"]

    # Send the transcription to Groq for summarization
    response = openai.ChatCompletion.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who summarizes long text into bullet points.",
            },
            {
                "role": "user",
                "content": f"Summarize the following:\n\n{text_to_summarize}",
            },
        ],
    )

    # Split the response into sentences
    summary = re.split(r"(?<=[.!?]) +", response["choices"][0]["message"]["content"])

    # Save summary to file
    with open("summary.txt", "w+", encoding="utf-8") as file:
        for sentence in summary:
            cleaned = sentence.strip()
            if cleaned:
                file.write("- " + cleaned + "\n")


if __name__ == "__main__":
    transcript_generator()
