import requests
from typing import List, Dict, Optional
import re


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_ids(query: str) -> List[str]:
    """Fetch PubMed IDs based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 50
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch paper details using PubMed IDs."""
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    response = requests.get(FETCH_URL, params=params)
    response.raise_for_status()
    return response.json().get("result", {})

def identify_non_academic_authors(paper_data: Dict) -> Optional[Dict]:
    """Extract non-academic author details based on heuristics."""
    authors = paper_data.get("authors", [])
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
