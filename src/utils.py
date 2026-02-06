from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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
    prompt_path = PROJECT_ROOT / "prompts" / filename
    return prompt_path.read_text(encoding="utf-8")
