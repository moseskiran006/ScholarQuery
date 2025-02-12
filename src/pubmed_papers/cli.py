# src/pubmed_papers/cli.py
import argparse
import logging
import sys
from typing import Optional
from .paper_fetcher import PubMedFetcher

def setup_logging(debug: bool) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main() -> None:
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Fetch research papers from PubMed with company affiliations'
    )
    
    parser.add_argument(
        'query',
        help='PubMed search query'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Output file path (CSV format)'
    )

    parser.add_argument(
        '-e', '--email',
        type=str,
        default="121ad0018@iiitk.ac.in", 
        help='Email address for PubMed API'
    )

    args = parser.parse_args()
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    try:
        # Initialize fetcher with email
        fetcher = PubMedFetcher(email=args.email)
        
        # Fetch papers
        papers = fetcher.fetch_papers(args.query)
        if not papers:
            logger.info("No matching papers found.")
            return

        if args.file:
            # Save to file
            fetcher.save_to_csv(papers, args.file)
        else:
            # Print to console
            for paper in papers:
                print("\n--- Paper ---")
                print(f"PubMed ID: {paper['pubmed_id']}")
                print(f"Title: {paper['title']}")
                print(f"Publication Date: {paper['publication_date']}")
                print(f"Non-academic Authors: {', '.join(paper['non_academic_authors'])}")
                print(f"Company Affiliations: {', '.join(paper['company_affiliations'])}")
                print(f"Corresponding Author Email: {paper['corresponding_author_email']}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()