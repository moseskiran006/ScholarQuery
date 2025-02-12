# src/pubmed_papers/paper_fetcher.py
from typing import List, Dict, Optional, TypedDict, Any
import logging
from Bio import Entrez
import pandas as pd
import re
from dataclasses import dataclass
import time

@dataclass
class PaperAuthor:
    name: str
    affiliation: Optional[str]
    email: Optional[str]
    is_academic: bool

class PaperInfo(TypedDict):
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_author_email: Optional[str]

class PubMedFetcher:
    def __init__(self, email: str):
        """Initialize the PubMed fetcher with your email (required by NCBI)."""
        Entrez.email = email
        self.logger = logging.getLogger(__name__)

    def _is_academic_affiliation(self, affiliation: str) -> bool:
        """Check if an affiliation is academic based on keywords."""
        academic_keywords = [
            'university', 'college', 'institut', 'school', 
            'hospital', 'medical center', 'laboratory', 
            'academy', 'faculty'
        ]
        # Convert to lowercase for case-insensitive comparison
        affiliation_lower = affiliation.lower()
        return any(keyword.lower() in affiliation_lower for keyword in academic_keywords)

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text using regex."""
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def _get_author_info(self, author: Dict[str, Any]) -> PaperAuthor:
        """Extract author information from PubMed author data."""
        # Get author name
        if 'LastName' in author and 'ForeName' in author:
            name = f"{author['ForeName']} {author['LastName']}"
        else:
            name = author.get('CollectiveName', 'Unknown Author')

        # Get affiliation
        affiliation = ''
        if 'AffiliationInfo' in author and author['AffiliationInfo']:
            affiliation = author['AffiliationInfo'][0].get('Affiliation', '')

        # Extract email from affiliation if present
        email = self._extract_email(affiliation)

        # Check if academic
        is_academic = self._is_academic_affiliation(affiliation) if affiliation else True

        return PaperAuthor(
            name=name,
            affiliation=affiliation,
            email=email,
            is_academic=is_academic
        )

    def fetch_papers(self, query: str, max_results: int = 100) -> List[PaperInfo]:
        """
        Fetch papers from PubMed based on the query.
        
        Args:
            query: PubMed search query
            max_results: Maximum number of results to return
            
        Returns:
            List of paper information dictionaries
        """
        self.logger.info(f"Fetching papers for query: {query}")
        
        try:
            # Search PubMed
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                sort="relevance"
            )
            record = Entrez.read(handle)
            handle.close()

            if not record["IdList"]:
                self.logger.info("No papers found for the given query.")
                return []

            paper_ids = record["IdList"]
            results: List[PaperInfo] = []

            # Fetch details for each paper
            for i, paper_id in enumerate(paper_ids):
                try:
                    # Add delay to respect NCBI's rate limits
                    if i > 0:
                        time.sleep(0.34)  # Maximum 3 requests per second

                    handle = Entrez.efetch(
                        db="pubmed",
                        id=paper_id,
                        rettype="medline",
                        retmode="xml"
                    )
                    paper = Entrez.read(handle)['PubmedArticle'][0]
                    handle.close()

                    article = paper['MedlineCitation']['Article']
                    
                    # Initialize paper data
                    non_academic_authors = []
                    company_affiliations = set()
                    corresponding_email = None

                    # Process authors
                    if 'AuthorList' in article:
                        for author in article['AuthorList']:
                            author_info = self._get_author_info(author)
                            
                            if not author_info.is_academic:
                                non_academic_authors.append(author_info.name)
                                if author_info.affiliation:
                                    company_affiliations.add(author_info.affiliation)
                            
                            if author_info.email and not corresponding_email:
                                corresponding_email = author_info.email

                    # Get publication date
                    pub_date = article['Journal']['JournalIssue']['PubDate']
                    year = pub_date.get('Year', '')
                    month = pub_date.get('Month', '')
                    publication_date = f"{month} {year}".strip()

                    # Only include papers with non-academic authors
                    if non_academic_authors:
                        paper_info: PaperInfo = {
                            'pubmed_id': paper_id,
                            'title': article['ArticleTitle'],
                            'publication_date': publication_date,
                            'non_academic_authors': non_academic_authors,
                            'company_affiliations': list(company_affiliations),
                            'corresponding_author_email': corresponding_email
                        }
                        results.append(paper_info)
                        self.logger.debug(f"Processed paper {paper_id}")

                except Exception as e:
                    self.logger.error(f"Error processing paper {paper_id}: {str(e)}")
                    continue

            self.logger.info(f"Found {len(results)} papers with company affiliations")
            return results

        except Exception as e:
            self.logger.error(f"Error fetching papers: {str(e)}")
            return []

    def save_to_csv(self, papers: List[PaperInfo], filename: str) -> None:
        """Save paper information to CSV file."""
        if not papers:
            self.logger.warning("No papers to save")
            return

        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        self.logger.info(f"Results saved to {filename}")