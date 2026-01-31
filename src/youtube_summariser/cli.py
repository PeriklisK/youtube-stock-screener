import argparse
import sys
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

# from . import __version__
from .llm_client import LLMClient
from .youtube_helper import YouTubeHelper
from .youtube_helper import YouTubeClient

load_dotenv()

SYSTEM_PROMPT = """Analyze the following YouTube transcript for stock or market recommendations. 

For every ticker or company mentioned as a "buy," "watch," or "recommendation," extract the information in the following format:

- **[TICKER/STOCK NAME]**: [A concise 1-2 sentence explanation of the specific technical or fundamental reasons given by the speaker for this recommendation.]

Guidelines:
1. If no specific stocks are recommended, return: "No specific stock recommendations found."
2. Focus on "why" (e.g., "breaking out of a wedge," "strong earnings beat," "moving average cross").
3. Ignore stocks mentioned in passing that aren't being actively recommended.

TRANSCRIPT:"""


def summarize_transcript(transcript: str, llm: LLMClient, stream: bool = True) -> str:
    """
    Summarize transcript using the configured LLM.

    Args:
        transcript: The video transcript to summarize
        llm: The LLM client instance
        stream: If True, use streaming and print output incrementally

    Returns:
        The complete summary text
    """
    if stream:
        # Use streaming and collect the full response
        summary_parts = []
        print("\n--- Summary ---\n")
        try:
            for chunk in llm.stream_chat(SYSTEM_PROMPT, transcript):
                print(chunk, end="", flush=True)
                summary_parts.append(chunk)
            print("\n")
            return "".join(summary_parts)
        except KeyboardInterrupt:
            print("\n\nSummary generation interrupted by user.")
            return "".join(summary_parts)
    else:
        # Non-streaming fallback
        return llm.chat(SYSTEM_PROMPT, transcript)


def generate_output_filename(video_id: str) -> str:
    """Generate a default output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"summary_{video_id}_{timestamp}.txt"


def get_transcripts_from_video_ids(collected_videos):
    master_data = []

    print(f"\nFound {len(collected_videos)} videos. Fetching transcripts...")

    for video in collected_videos:
        try:
            raw = YouTubeHelper.get_transcript(video['v_id'])
            if isinstance(raw, str):
                # If your helper already joins the text into a string, use it directly
                full_text = raw 
            else:
                # If it's the raw list of dicts, join it here
                full_text = "\n".join([t['text'] for t in raw])
                
            master_data.append({
                "channel": video['channel'],
                "title": video['title'],
                "transcript": full_text
            })
            print(f"✅ Success: {video['title']}")
            wait_time = random.uniform(5, 12)
            print(f"Sleeping for {wait_time:.2f}s to avoid IP block...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ Failed transcript for {video['title']}")
            print(e)
            raise
    return master_data


def combine_transcripts(master_data):
    context_for_gemini = ""
    for entry in master_data:
        context_for_gemini += f"\nSOURCE CHANNEL: {entry['channel']}\n"
        context_for_gemini += f"VIDEO TITLE: {entry['title']}\n"
        context_for_gemini += f"TRANSCRIPT CONTENT: {entry['transcript']}\n"
        context_for_gemini += "--- END OF TRANSCRIPT ---"
        context_for_gemini += "="*10 + "\n"    
        return context_for_gemini


def load_prompt(filename: str) -> str:
    current_script = Path(__file__).resolve()
    project_root = current_script.parent.parent.parent
    prompt_path = project_root / "prompts" / filename
    return prompt_path.read_text(encoding="utf-8")


def main():
    channels = {
        "BWB - Business With Brian": "UULFyqlbzLoYtpqDXwRI9Yh5LA",
        "Chris Sain": "UULFrTFPf6rq5OUSWb7ILW9trg",
        "Asymmetric Investing by Travis Hoium": "UULFM2udYo4m-_uQfbfLGwf6mA",
        "Felix & Friends (Goat Academy)": "UULFJtfma0mE_XrBAD9uakcjfA",
        "Amit Kukreja": "UULFjZnbgPb08NFg7MHyPQRZ3Q",
    }

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    system_prompt = load_prompt("combined_transcript_summary.md")

    yt_client = YouTubeClient()
    video_ids = yt_client.get_video_ids_from_channels(channels, start_date_str, end_date_str)
    print(video_ids)
    transcripts = get_transcripts_from_video_ids(video_ids)
    llm_context = combine_transcripts(transcripts)
    llm = LLMClient(provider="google")
    final_report = llm.chat(system_prompt=system_prompt, user_message=llm_context) 
    with open(f"reports/{start_date_str}_report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)


if __name__ == "__main__":
    main()
