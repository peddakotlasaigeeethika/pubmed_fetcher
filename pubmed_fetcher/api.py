import requests
import csv
from typing import List, Dict, Optional
from requests.exceptions import RequestException

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_ids(query: str) -> List[str]:
    params = {
        "db": "pubmed",
        "term": f'"{query}"[ti]',
        "retmode": "json",
        "retmax": 50
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):
            print("ERROR: Invalid API response format.")
            return []

        pubmed_ids = data.get("esearchresult", {}).get("idlist", [])
        print("DEBUG: PubMed IDs fetched:", pubmed_ids)

        if not pubmed_ids:
            print(f"No papers found for query: {query}")
            return []

        return pubmed_ids

    except RequestException as e:
        print(f"ERROR: Failed to fetch PubMed IDs: {e}")
        return []

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }

    try:
        response = requests.get(FETCH_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            print("ERROR: Invalid response format from PubMed API.")
            return []

        papers = []
        for paper_id, details in data.get("result", {}).items():
            if paper_id == "uids":
                continue
            papers.append({
                "pubmed_id": paper_id,
                "title": details.get("title", "Unknown"),
                "publication_date": details.get("pubdate", "Unknown"),
                "authors": details.get("authors", []),
            })

        return papers

    except RequestException as e:
        print(f"ERROR: Failed to fetch paper details: {e}")
        return []

def identify_non_academic_authors(paper_data: Dict) -> Optional[Dict]:
    if not isinstance(paper_data, dict):
        print("ERROR: Expected dictionary but got:", type(paper_data))
        return None

    authors = paper_data.get("authors", [])

    if not isinstance(authors, list):
        print("ERROR: Expected authors to be a list but got:", type(authors))
        return None

    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if not any(keyword in affiliation for keyword in ["university", "college", "institute", "school", "hospital", "clinic"]):
            non_academic_authors.append(author.get("name"))
            company_affiliations.append(affiliation)

    if non_academic_authors:
        return {
            "authors": non_academic_authors,
            "affiliations": company_affiliations
        }
    return None

def save_results_to_csv(papers: List[Dict], filename: str = "results.csv"):
    if not papers:
        print("No papers to save. Skipping CSV file creation.")
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["pubmed_id", "title", "publication_date", "authors"])
            writer.writeheader()
            writer.writerows(papers)
        print(f"Results saved to {filename}")

    except Exception as e:
        print(f"ERROR: Failed to write to {filename}: {e}")

if __name__ == "__main__":
    query = "cancer research"
    pubmed_ids = fetch_pubmed_ids(query)
    
    if not pubmed_ids:
        print("No papers found. Exiting program.")
    else:
        papers = fetch_paper_details(pubmed_ids)
        save_results_to_csv(papers)
