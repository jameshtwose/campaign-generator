from google_news_feed import GoogleNewsFeed
import subprocess
import requests
from datetime import date, timedelta
import platform

if platform.system() == "Darwin":
    # macOS: use whisper-mps
    from whisper_mps.whisper.transcribe import transcribe as whisper_transcribe

    def transcribe_audio(file_path: str):
        """Transcribe audio file to text using whisper_mps."""
        result = whisper_transcribe(file_path, model="small")
        return result["text"]
else:
    # Linux/other: use faster-whisper
    from faster_whisper import WhisperModel

    def transcribe_audio(file_path: str):
        """Transcribe audio file to text using faster-whisper."""
        model = WhisperModel("small")
        segments, info = model.transcribe(file_path)
        # Concatenate all segments
        return " ".join([segment.text for segment in segments])


def get_ollama_host():
    if platform.system() == "Darwin":
        print("Using localhost for Ollama API")
        return "http://localhost:11434"
    else:
        print("Using Docker container for Ollama API")
        return "http://ollama:11434"


def get_ollama_questions(text: str, model: str = "gemma3:1b"):
    """Generate a list of questions based on the prompt text using Ollama API."""
    url = f"{get_ollama_host()}/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates questions based on text.",
            },
            {
                "role": "system",
                "content": "Return a list of questions in formatted HTML.",
            },
            {"role": "system", "content": "Use <ul> and <li> tags for the questions."},
            {
                "role": "system",
                "content": "Only respond with the HTML content, no explanations.",
            },
            {"role": "user", "content": text},
        ],
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    generated_text = response.json()["choices"][0]["message"]["content"]

    # Remove markdown code block markers if present
    if generated_text.startswith("```html"):
        generated_text = generated_text[len("```html") :].strip()
    if generated_text.endswith("```"):
        generated_text = generated_text[:-3].strip()
    return generated_text


def get_ollama_summary(text: str, model: str = "gemma3:1b"):
    """Get a summary of the text using Ollama API."""
    url = f"{get_ollama_host()}/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "system",
                "content": "Please return the output in formatted html.",
            },
            {
                "role": "system",
                "content": "Use HTML tags like <p>, <b>, <i>, <ul>, <li> for formatting.",
            },
            {"role": "system", "content": "Use nice css styles to make it look cool."},
            {
                "role": "system",
                "content": "Only respond with the HTML content, no explanations.",
            },
            {"role": "user", "content": text},
        ],
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    generated_text = response.json()["choices"][0]["message"]["content"]

    # Remove markdown code block markers if present
    if generated_text.startswith("```html"):
        generated_text = generated_text[len("```html") :].strip()
    if generated_text.endswith("```"):
        generated_text = generated_text[:-3].strip()
    return generated_text


def convert_webm_to_mp3(webm_path, mp3_path):
    subprocess.run(["ffmpeg", "-y", "-i", webm_path, mp3_path], check=True)


def get_latest_news(topic: str, num_results: int = 5):
    """Fetch the latest news updates on a topic using google-news-feed."""
    feed = GoogleNewsFeed()
    results = feed.query(
        query=topic, before=date.today(), after=date.today() - timedelta(days=7)
    )
    news_list = [
        {
            "title": getattr(item, "title", None),
            "link": getattr(item, "link", None),
            "published": getattr(item, "published", None),
        }
        for item in results[:num_results]
    ]
    return news_list
