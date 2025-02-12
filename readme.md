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
git clone https://github.com/yourusername/pubmed-papers.git
cd pubmed-papers
```

3. Install dependencies:
```bash
poetry install
```

## Usage

The package provides a command-line tool `get-papers-list`:

```bash
# Basic usage
poetry run get-papers-list "cancer therapy"

# Save results to file
poetry run get-papers-list "cancer therapy" -f results.csv

# Enable debug logging
poetry run get-papers-list "cancer therapy" -d

# Show help
poetry run get-papers-list --help
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

