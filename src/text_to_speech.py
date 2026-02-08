import asyncio
import edge_tts
from .utils import PROJECT_ROOT

async def _generate_voice_async(text, path):
    communicate = edge_tts.Communicate(text, "en-US-AvaNeural")
    await communicate.save(path)


def text_to_voice(text, filename="output.mp3"):
    full_path = PROJECT_ROOT/ "reports" / filename
    asyncio.run(_generate_voice_async(text, full_path))
    return full_path
