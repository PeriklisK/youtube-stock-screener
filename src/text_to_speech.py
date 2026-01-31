import asyncio
import edge_tts


async def _generate_voice_async(text, filename):
    communicate = edge_tts.Communicate(text, "en-US-AvaNeural")
    await communicate.save(filename)


def text_to_voice(text, filename="output.mp3"):
    asyncio.run(_generate_voice_async(text, filename))

# --- MAIN EXECUTION ---
summary = "If you plan on adding more modern features later (like downloading transcripts while summarizing at the same time), it's better to make your whole script async. This is the industry standard for 2026."  # Normal sync call
text_to_voice(summary)         # This runs the async part and waits for it
print("All done!")