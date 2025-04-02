# Entity Validation System (EVS)

A robust data validation system for ensuring entity names conform to standardized naming conventions and preventing duplication before bulk uploads.

## Overview

The Entity Validation System (EVS) is designed to perform a multi-stage validation process to enhance data consistency and integrity:

1. **Standardization and preparation** : When a file is first uploaded it is standardized and checked for internal duplicates.
2. **Naming Convention Compliance** : All entities are validated against predefined naming standards.
3. **Duplicate Prevention** : Entities are matched against existing authorized records to prevent duplication.
4. **New Entity Identification** : Potential new entities are identified based on partial matches and can be added to the authoritative list.

## Features

* **Intuitive GUI** with a tab-based interface for file uploads and validation review
* **Multi-threaded processing** to prevent UI freezing during operations
* **Advanced fuzzy matching** with configurable thresholds
* **Interactive decision management** for handling validation issues
* **Comprehensive reporting** of validation results
* **Batch processing mode** for automated validation through command line
* **Configurable validation rules** for naming conventions
* **Detailed logging** for troubleshooting and audit purposes

## Installation

### Prerequisites

* Python 3.8 or higher
* Required packages listed in `requirements.txt`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/entity_validation_system.git
   cd entity_validation_system
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode

To start the application in GUI mode:

```bash
python src/main.py
```

The GUI consists of four tabs:

1. **Setup** : Configure file paths and validation settings
2. **Validation** : Review and manage naming convention validation results
3. **Duplicates** : Detect and resolve duplicate entities
4. **Reports** : Generate and view validation reports

### Command-Line Mode

For batch processing without GUI:

```bash
python src/main.py --batch --input input.csv --auth-list auth_entities.csv
```

#### Command-Line Options

* `--batch`: Run in batch mode without GUI
* `--input`: Input CSV file path
* `--auth-list`: Authoritative entity list CSV file path
* `--output-dir`: Output directory for reports (default: 'reports')
* `--column`: Entity column name (default: 'name')
* `--threshold`: Matching threshold (0-1, default: 0.85)
* `--update-original`: Update original file with corrections
* `--log-level`: Logging level (default: INFO)
* `--log-file`: Log file path (default: auto-generated)

Example with all options:

```bash
python src/main.py --batch --input data/input.csv --auth-list data/AuthoritativeEntityList.csv --output-dir reports --column name --threshold 0.9 --update-original --log-level DEBUG --log-file logs/validation.log
```

## Naming Convention Standards

The system enforces the following naming standards:

1. **Full Names** : Use complete entity names (e.g., "National Aeronautics and Space Administration" instead of "NASA").
2. **Ampersand Usage** : Replace "&" with "and" (e.g., "Johnson and Johnson").
3. **Apostrophe Removal** : Omit apostrophes in possessives (e.g., "3Es" instead of "3E's").
4. **No special characters** : Special characters are removed, with exceptions for government entities.
5. **Business Designations** : Terms like "LLC," "Inc.," etc. are excluded.
6. **Company Naming** : "Company" is spelled out instead of abbreviated as "Co".
7. **Government Entity Formatting** :

* State: "State of California"
* County: "County of Pinellas (FL)"
* City/Town: "City of Tampa (FL)"

## Input Requirements

* **Input Format** : CSV files containing entity data
* **Required Fields** : At least one of the following must be present:
* "name"
* "facility"
* "owner"
* "operator"
* **Reference Data** : Primary reference file is `AuthoritativeEntityList.csv`

## Directory Structure

```
entity_validation_system/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── naming_convention.py
│   │   ├── duplicate_detection.py
│   │   └── validation_rules.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_handling.py
│   │   └── fuzzy_matching.py
│   │
│   └── gui/
│       ├── __init__.py
│       ├── validation_frame.py
│       ├── duplicate_frame.py
│       └── report_frame.py
│
├── data/
│   └── AuthoritativeEntityList.csv
│
├── docs/
│   └── user_manual.md
│   
├── logs/
│   └── (log files generated during runtime)
│
├── reports/
│   └── (reports generated during validation)
│
├── requirements.txt
│
└── README.md
```

## Development

### Adding New Validation Rules

To add new validation rules, modify the `ValidationRules` class in `src/validation/validation_rules.py`. Each rule should have:

1. A method to check if an entity violates the rule
2. A method to correct violations of the rule
3. Integration into the `apply_all_rules` method

### Extending Fuzzy Matching

The fuzzy matching capabilities can be extended in `src/utils/fuzzy_matching.py` by:

1. Adding new matching algorithms
2. Adjusting weighting for the combined similarity score
3. Adding new pre-processing techniques

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

* Levenshtein Distance algorithm for string similarity
* Soundex and Metaphone algorithms for phonetic matching
* TF-IDF vectorization for token-based matching
