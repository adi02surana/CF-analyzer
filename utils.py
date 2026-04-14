import datetime

def format_timestamp(timestamp: int) -> str:
    """Convert Unix timestamp to a readable date (YYYY-MM-DD)."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def print_header(title: str):
    """Prints a styled header."""
    print("\n" + "="*50)
    print(f" {title} ")
    print("="*50)

def print_insight(insight: str):
    """Prints an insight message."""
    print(f"🧠 INSIGHT: {insight}")
