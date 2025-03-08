import pandas as pd
from typing import List, Dict

def save_to_csv(papers: List[Dict], filename: str):
    """Save research paper data to CSV format."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
