from .utils import PROJECT_ROOT
from .schemas import StockEntry

def load_prompt(filename: str) -> str:
    """Reads a template from the /prompts directory."""
    with open(PROJECT_ROOT/ "prompts" / filename, "r", encoding="utf-8") as f:
        return f.read()
    

def load_formated_stock_prompt(stock: StockEntry):
    ticker_prompt_template = load_prompt("generate_transcript_for_ticker.md")
    # print(f"Generating prompt for {len(report.stocks)} stock...")
    # for stock in report.stocks:
    print(f"-> Processing {stock.ticker}...")    
    metrics_str = ", ".join([f"{m.label}: {m.value}" for m in stock.metrics])

    # Inject variables into the template
    script_prompt = ticker_prompt_template.format(
        ticker=stock.ticker,
        company_name=stock.company_name,
        sentiment=stock.sentiment,
        thesis=stock.thesis,
        metrics_str=metrics_str
    )
    return script_prompt
        

def save_json(report, filename):
    json_data = report.model_dump_json(indent=2)
    with open(PROJECT_ROOT/ "reports" / filename, "w", encoding="utf-8") as f:
        f.write(json_data)