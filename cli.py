import click
from .api import fetch_pubmed_ids, fetch_paper_details, identify_non_academic_authors
from .output import save_to_csv

@click.command()
@click.argument("query")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
@click.option("-f", "--file", type=str, help="Filename to save results")
def get_papers_list(query: str, debug: bool, file: Optional[str]):
    """Fetch and filter research papers from PubMed."""
    if debug:
        click.echo(f"Fetching papers for query: {query}")

    pubmed_ids = fetch_pubmed_ids(query)
    papers = fetch_paper_details(pubmed_ids)

    filtered_papers = []
    for paper in papers.values():
        filtered_authors = identify_non_academic_authors(paper)
        if filtered_authors:
            filtered_papers.append({
                "PubmedID": paper.get("uid"),
                "Title": paper.get("title"),
                "Publication Date": paper.get("pubdate"),
                "Non-academic Author(s)": ", ".join(filtered_authors["authors"]),
                "Company Affiliation(s)": ", ".join(filtered_authors["affiliations"]),
                "Corresponding Author Email": paper.get("email", "N/A")
            })

    if file:
        save_to_csv(filtered_papers, file)
    else:
        click.echo(filtered_papers)

if __name__ == "__main__":
    get_papers_list()
