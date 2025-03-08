# PubMed Research Paper Fetcher

A Python command-line tool to fetch research papers from PubMed, identify non-academic authors affiliated with pharmaceutical or biotech companies, and export results as a CSV file.

## Features
-Fetches research papers from PubMed API using a flexible query.
-Filters papers with at least one non-academic author (e.g., pharmaceutical/biotech affiliations).
-Outputs results as a CSV file with key details:
-PubMed ID
-Title
-Publication Date
-Non-Academic Author(s)
-Company Affiliation(s)
-Corresponding Author Email
# Project Structure

->pubmed_fetcher  
  -> pubmed_fetcher  
   ->__init__.py       
   ->api.py           
   -> cli.py            
   -> output.py       
 -> tests         
 -> pyproject.toml     # Poetry configuration file   
 -> README.md          # Documentation  

## Tools and Libraries Used

-PubMed API – Fetches research papers.
-Poetry – Dependency management and packaging.
-Click – CLI framework for handling user input.
-Requests – Makes API requests.
-Pandas – Processes tabular data for CSV output.



## Example Output (CSV Format)

| PubMed ID | Title                 | Publication Date | Non-Academic Author(s) | Company Affiliation(s) | Corresponding Email  |
|-----------|--------------------- -|------------------|------------------------|------------------------|----------------------|
| 12345678  | Gene Therapy in 2024  | 2024-01-01       | John Doe               | ABC Biotech Inc.       | johndoe@abc.com     |
| 23456789  | New Advances in Cancer| 2023-05-15       | Jane Smith             | XYZ Pharmaceuticals    | janesmith@xyz.com   |



 