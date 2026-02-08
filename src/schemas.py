from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class StockMetric(BaseModel):
    label: str
    value: str

class StockEntry(BaseModel):
    ticker: str
    company_name: str
    sentiment: Literal["Bullish", "Bearish", "Neutral"]
    thesis: str
    sources: List[str]
    metrics: List[StockMetric]
    voiceover_script: Optional[str] = None
    # voiceover_script: Optional[str] = Field(default=None, exclude=True)

class MarketReport(BaseModel):
    report_title: str
    audio_path: str
    stocks: List[StockEntry]
