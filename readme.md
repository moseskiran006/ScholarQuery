# ScholarQuery – A smart querying tool for research.


## PubMed Papers

A Python package to fetch research papers from PubMed and identify papers with authors affiliated with pharmaceutical or biotech companies.

## Features

- Search PubMed using their full query syntax
- Identify papers with non-academic authors
- Export results to CSV or display in console
- Command-line interface with debug options
- Fully typed Python code

## Installation

This package uses Poetry for dependency management. To install:

1. Make sure you have Poetry installed:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone https://github.com/moseskiran006/pubmed-papers.git
cd pubmed-papers
```

3. Install dependencies:
```bash
poetry install
```

## Usage

The package provides a command-line tool `get-papers-list`:

# Basic search
```
python -m pubmed_papers.cli "cancer therapy"
```
# Save to CSV file
```
python -m pubmed_papers.cli "cancer therapy" -f results.csv
```
# Debug mode
```
python -m pubmed_papers.cli "cancer therapy" -d
```
# Complex search
```
python -m pubmed_papers.cli "cancer AND therapy AND (pharma OR biotech)"
```
## Code Organization

The package is organized as follows:

```
pubmed-papers/
├── pyproject.toml          # Poetry configuration and dependencies
├── README.md              # This file
└── src/
    └── pubmed_papers/
        ├── __init__.py
        ├── paper_fetcher.py  # Core functionality for fetching papers
        └── cli.py           # Command-line interface
```

## Tools and Libraries Used

- [Poetry](https://python-poetry.org/) - Dependency management and packaging
- [Biopython](https://biopython.org/) - Interface to PubMed/NCBI API
- [pandas](https://pandas.pydata.org/) - Data handling and CSV export
- [typing](https://docs.python.org/3/library/typing.html) - Type hints
- [logging](https://docs.python.org/3/library/logging.html) - Debug and error logging

## Development

This project uses:
- Type hints throughout the codebase
- Modular design with separation of concerns
- Error handling for robustness
- Logging for debugging
- Clear documentation and docstrings

## License

MIT

