import operator
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END

from .llm_client import LLMClient
from .youtube_helper import YouTubeHelper, YouTubeClient
from .text_to_speech import text_to_voice 
from .utils import load_prompt, combine_transcripts
from .cli import get_transcripts_from_video_ids

class AgentState(TypedDict):
    channels: List[str]
    start_date: str
    end_date: str
    video_ids: List[str]
    transcripts: List[str]
    summary: str
    audio_path: str
    # 'errors' allows the agent to track what went wrong
    errors: List[str]

def get_videos_node(state: AgentState):
    yt = YouTubeClient()
    channels = state["channels"]
    sd = state["start_date"]
    ed = state["end_date"]    
    ids = yt.get_video_ids_from_channels(channels, sd, ed)
    return {"video_ids": ids}

def transcript_node(state: AgentState):
    try:
        # yt_client = YouTubeClient()
        data = get_transcripts_from_video_ids(state["video_ids"])
        return {"transcripts": data}
    except Exception as e:
        return {"errors": [f"Transcript failed: {e}"]}

def summarize_node(state: AgentState):
    system_prompt = load_prompt("combined_transcript_summary.md")
    llm = LLMClient(provider="google")
    llm_context = combine_transcripts(state["transcripts"])
    # print(system_prompt)
    print("\n\n\n")
    print(llm_context)
    report = llm.chat(system_prompt=system_prompt, user_message=llm_context) 
    return {"summary": report}

def voiceover_node(state: AgentState):
    path = f"reports/audio.mp3"
    text_to_voice(state["summary"], path)
    return {"audio_path": path}


workflow = StateGraph[AgentState, None, AgentState, AgentState](AgentState)

# Add our nodes
workflow.add_node("fetch_videos", get_videos_node)
workflow.add_node("fetch_transcripts", transcript_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("voiceover", voiceover_node)

# Define the flow
workflow.add_edge(START, "fetch_videos")
workflow.add_edge("fetch_videos", "fetch_transcripts")
workflow.add_edge("fetch_transcripts", "summarize")
workflow.add_edge("summarize", "voiceover")
workflow.add_edge("voiceover", END)

# Compile
app = workflow.compile()