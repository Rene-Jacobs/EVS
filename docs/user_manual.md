# Entity Validation System (EVS) - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [GUI Mode](#gui-mode)
   - [Setup Tab](#setup-tab)
   - [Validation Tab](#validation-tab)
   - [Duplicates Tab](#duplicates-tab)
   - [Reports Tab](#reports-tab)
5. [Command-Line Mode](#command-line-mode)
6. [Understanding Validation Rules](#understanding-validation-rules)
7. [Fuzzy Matching Explained](#fuzzy-matching-explained)
8. [Reports and Output Files](#reports-and-output-files)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)
11. [FAQ](#faq)
12. [Glossary](#glossary)

---

## Introduction

The Entity Validation System (EVS) is a professional-grade tool designed to ensure data quality and consistency by validating entity names against standardized naming conventions and preventing duplicate entries. It is especially valuable when preparing data for bulk uploads to enterprise systems.

### Key Benefits

- **Data Standardization**: Ensures all entity names follow consistent naming conventions
- **Duplicate Prevention**: Identifies potential duplicates before they enter your systems
- **Efficiency**: Reduces manual review through automated validation
- **Auditability**: Maintains detailed logs of all validation decisions
- **Quality Assurance**: Improves overall data quality in your systems

### Use Cases

- Data migration projects
- Regular data imports to enterprise systems
- Validation of third-party data
- Data cleansing initiatives
- Establishing authoritative entity lists

---

## Installation

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB+ recommended for large datasets)
- **Disk Space**: 500MB for installation, plus space for your data and reports
- **Display**: 1280x720 or higher resolution

### Installation Steps

1. **Python Installation**:

   - If Python isn't already installed, download and install it from [python.org](https://python.org)
   - Ensure you select the option to add Python to PATH during installation on Windows
2. **EVS Installation**:

   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/entity_validation_system.git
   cd entity_validation_system

   # Create a virtual environment (recommended)
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```
3. **Verify Installation**:

   ```bash
   python src/main.py --help
   ```

   This should display the help information for the application.

---

## Getting Started

### Preparing Your Data

EVS works with CSV files containing entity data. Your input file should have at least one of the following columns:

- `name`: The entity name
- `facility`: Facility name
- `owner`: Owner entity name
- `operator`: Operator entity name

Column names are case-insensitive and spaces will be converted to underscores.

### Authoritative Entity List

The system compares your input entities against an authoritative list stored in:

```
data/AuthoritativeEntityList.csv
```

Ensure this file exists and contains the proper reference data. If you need to specify a different file, you can do so through the GUI or command-line options.

### Basic Workflow

1. Prepare your CSV file with entity data
2. Run EVS in GUI or command-line mode
3. Review validation results
4. Make decisions on naming convention issues and duplicates
5. Generate reports
6. Apply corrections to your data

---

## GUI Mode

To start the application in GUI mode:

```bash
python src/main.py
```

The EVS interface consists of four tabs representing the validation workflow:

### Setup Tab

The Setup tab is your starting point, where you configure the validation process:

#### File Selection

- **Input File**: Click "Browse..." to select your input CSV file.
- **Authoritative List**: Click "Browse..." to select the authoritative entity list. By default, it will use `data/AuthoritativeEntityList.csv`.

#### Configuration

- **Entity Column**: Select which column contains the entity names to validate.
- **Matching Threshold**: Adjust the slider to set the sensitivity of duplicate detection:

  - Higher values (closer to 100%) require closer matches
  - Lower values (closer to 50%) will find more potential duplicates but increase false positives
  - **Enable Advanced Matching**: Activates more sophisticated but computationally intensive matching algorithms.

    When "Enable Advanced Matching" is NOT checked: The system uses a combination of:

    1.**Levenshtein Distance**: Measures the minimum number of single-character edits (insertions, deletions, substitutions) required to change one string into another.

    2.**Token-Based Matching**: Compares word tokens rather than character-by-character, useful for rearranged words.

    3.**Soundex Matching**: Uses the Soundex algorithm to match words that sound similar.

    4.**Metaphone Matching**: Another phonetic matching algorithm that is more accurate than Soundex for many cases.

    When "Enable Advanced Matching" IS checked: The system uses all the methods above plus:

    5.**Machine Learning-Based Matching**: Uses neural network embeddings to capture semantic similarity.
    The ML-based matching relies on TensorFlow and specifically uses a Universal Sentence Encoder model that creates vector embeddings to measure semantic
    similarity between entity names. This more sophisticated approach can detect matches that the other methods might miss, but is more computationally intensive.

#### Starting Validation

1. Select your input file and verify the authoritative list location
2. Configure your settings
3. Click "Start Validation" to begin the process

The system will first process naming conventions and then move to the Validation tab automatically.

### Validation Tab

The Validation tab displays naming convention violations and allows you to review and resolve them:

#### Validation Status

The top section shows:

- Current validation status
- Progress bar during processing
- Summary statistics (total entities, valid count, invalid count)

#### Naming Convention Violations

The table displays entities that violate naming conventions:

- **Entity**: Original entity name
- **Violations**: List of specific rule violations
- **Suggestion**: System-suggested correction
- **Action**: Dropdown to select how to handle the violation
- **Status**: Current resolution status

#### Action Options

For each violation, you can:

- **Accept**: Use the suggested correction
- **Reject**: Keep the original name despite the violation
- **Modify**: Edit the suggestion to a custom value

#### Batch Actions

- **Accept All**: Apply all suggested corrections
- **Reject All**: Keep all original values
- **Apply Changes**: Finalize your decisions

After reviewing naming conventions, you'll be prompted to continue to duplicate detection.

### Duplicates Tab

The Duplicates tab has two sub-tabs:

#### Internal Duplicates

Shows potential duplicates within your input file:

- **Entity**: Entity name
- **Duplicate Group**: Group ID for related duplicates
- **Match**: Best matching entity
- **Score**: Similarity score (0-1)
- **Action**: How to resolve the duplicate group

##### Action Options for Internal Duplicates:

- **Keep Best**: Retain only the best entity from the group
- **Merge**: Combine information from all duplicates
- **Custom**: Specify a custom entity name

##### Batch Actions:

- **Resolve Selected Group**: Apply resolution to the selected group
- **Resolve All Groups**: Apply resolution to all groups

#### External Duplicates

Shows potential matches against the authoritative list:

- **Entity**: Your entity name
- **Auth Match**: Matching entity in the authoritative list
- **Score**: Similarity score (0-1)
- **Exact Match**: Whether it's an exact (100%) match
- **Action**: How to handle the match
- **Status**: Current resolution status

##### Action Options for External Duplicates:

- **Accept Match**: Use the authorized entity name
- **Reject Match**: Treat as a distinct entity
- **New Entity**: Add to the authoritative list

##### Batch Actions:

- **Accept All Matches**: Accept all suggested matches
- **Reject All Matches**: Reject all suggested matches

#### Finalizing Duplicate Detection

After reviewing both internal and external duplicates:

1. Click "Apply Changes" to save your decisions
2. Click "Continue to Reports" to proceed to report generation

### Reports Tab

The Reports tab allows you to generate comprehensive reports of the validation process:

#### Report Generation Status

Shows the current status of report generation and a progress bar.

#### Report Options

- **Update original file with validated entities**: Create a new version of your input file with corrections applied

#### Generate Reports

Click "Generate Reports" to create the following report types:

- Comprehensive report
- Unresolved issues report
- Audit log
- Updated file (if selected)
- Removed entries (if any)

#### Generated Reports

The list shows all generated reports with options to:

- Open a selected report
- Open the reports folder

All reports are saved in the `reports` directory by default.

---

## Command-Line Mode

For automation and batch processing, EVS provides a command-line interface:

### Basic Usage

```bash
python src/main.py --batch --input input.csv --auth-list auth_entities.csv
```

### Available Options

- `--batch`: Run in batch mode without GUI
- `--input`: Input CSV file path
- `--auth-list`: Authoritative entity list CSV file path
- `--output-dir`: Output directory for reports (default: 'reports')
- `--column`: Entity column name (default: 'name')
- `--threshold`: Matching threshold (0-1, default: 0.85)
- `--update-original`: Update original file with corrections
- `--log-level`: Logging level (default: INFO)
- `--log-file`: Log file path (default: auto-generated)

### Example with Full Options

```bash
python src/main.py --batch --input data/input.csv --auth-list data/AuthoritativeEntityList.csv --output-dir reports --column name --threshold 0.9 --update-original --log-level DEBUG --log-file logs/validation.log
```

### Output

The command-line mode produces the same reports as the GUI mode but operates without user interaction. It applies the following rules automatically:

- Naming convention violations: Applies all suggested corrections
- Internal duplicates: Keeps the entity with the fewest validation issues
- External duplicates: Accepts exact matches automatically

A summary is printed to the console upon completion, showing:

- Total entities processed
- Valid/invalid naming conventions
- Internal duplicate groups
- External matches
- Generated report files

---

## Understanding Validation Rules

EVS applies several naming convention rules to ensure consistency:

### 1. Full Names Instead of Acronyms

- **Rule**: Use complete entity names rather than acronyms
- **Example**: "National Aeronautics and Space Administration" instead of "NASA"
- **Rationale**: Full names prevent ambiguity and confusion

### 2. Ampersand Replacement

- **Rule**: Replace "&" with "and"
- **Example**: "Johnson and Johnson" instead of "Johnson & Johnson"
- **Rationale**: Standardizes text and prevents processing issues in some systems

### 3. Apostrophe Removal

- **Rule**: Remove apostrophes from possessives and contractions
- **Example**: "3Es" instead of "3E's"
- **Rationale**: Simplifies text processing and prevents inconsistencies

### 4. Special Character Removal

- **Rule**: Remove special characters (with exceptions for government entities)
- **Example**: "Alpha Beta" instead of "Alpha-Beta"
- **Rationale**: Ensures consistent formatting and prevents system issues

### 5. Business Designation Removal

- **Rule**: Exclude terms like "LLC," "Inc.," etc.
- **Example**: "Acme" instead of "Acme Inc."
- **Rationale**: Separates legal structure from the core entity name

### 6. Abbreviation Expansion

- **Rule**: Expand common abbreviations
- **Example**: "Acme Company" instead of "Acme Co."
- **Rationale**: Ensures consistency and clarity

### 7. Government Entity Formatting

- **Rule**: Follow specific patterns for government entities
- **Examples**:
  - "State of California"
  - "County of Pinellas (FL)"
  - "City of Tampa (FL)"
- **Rationale**: Standardizes government entities with clear jurisdictional information

---

## Fuzzy Matching Explained

EVS uses sophisticated fuzzy matching techniques to identify potential duplicates:

### Matching Techniques

The system employs multiple methods and combines their results:

#### 1. Levenshtein Distance

Measures the minimum number of single-character edits (insertions, deletions, substitutions) required to change one string into another.

**Example**: "Acme" and "Acme Corp" have a Levenshtein distance of 5 (5 character insertions)

#### 2. Token-Based Matching

Compares word tokens rather than character-by-character, useful for rearranged words.

**Example**: "Global Technologies Inc" and "Inc Global Technologies" would have high token similarity

#### 3. Phonetic Matching

Uses Soundex and Metaphone algorithms to match words that sound similar.

**Example**: "Kleiner" and "Kleyner" would match phonetically

#### 4. Machine Learning-Based Matching (Advanced)

When advanced matching is enabled, uses embedding models to capture semantic similarity.

### Matching Threshold

The matching threshold controls sensitivity:

- **Higher thresholds** (90%+): Conservative matching, fewer false positives
- **Medium thresholds** (80-90%): Balanced approach
- **Lower thresholds** (50-80%): Aggressive matching, may find more duplicates but also more false positives

### Pre-processing for Better Matching

Before comparison, entity names are:

1. Converted to lowercase
2. Stripped of business designations
3. Cleaned of special characters
4. Normalized with consistent spacing

---

## Reports and Output Files

EVS generates several types of reports:

### Comprehensive Report

- **Filename**: `comprehensive_report_YYYYMMDD_HHMMSS.csv`
- **Contents**: Complete validation results for all entities
- **Fields**:
  - Original entity data
  - Naming convention status and issues
  - Duplicate detection results
  - Resolution status

### Unresolved Issues Report

- **Filename**: `unresolved_issues_YYYYMMDD_HHMMSS.csv`
- **Contents**: Entities with remaining validation issues
- **Fields**:
  - Entity information
  - Specific unresolved issues
  - Suggestions for resolution

### Audit Log

- **Filename**: `audit_log_YYYYMMDD_HHMMSS.csv`
- **Contents**: Chronological record of all validation actions
- **Fields**:
  - Timestamp
  - Action type
  - Entity name
  - Action details

### Updated File

- **Filename**: `updated_file_YYYYMMDD_HHMMSS.csv`
- **Contents**: Original input data with corrections applied
- **When Generated**: If "Update original file" option is selected

### Removed Entries

- **Filename**: `removed_entries_YYYYMMDD_HHMMSS.csv`
- **Contents**: Entries removed due to being duplicates or invalid
- **When Generated**: If any entries are removed during validation

---

## Advanced Features

### Custom Validation Rules

EVS allows for customization of validation rules by modifying:

```
config/validation_rules.yaml
```

This configuration file controls:

- Business designations to remove
- Abbreviations to expand
- Government entity patterns
- Default thresholds

### Integrating with Other Systems

The command-line mode facilitates integration into data pipelines and automated workflows:

1. **Scheduled Validation**:

   ```bash
   # Example cron job to run validation daily
   0 1 * * * /path/to/python /path/to/evs/src/main.py --batch --input /path/to/daily_import.csv --auth-list /path/to/auth_list.csv --output-dir /path/to/reports
   ```
2. **Pre-processing for Data Imports**:

   ```bash
   # Example script to validate before import
   python src/main.py --batch --input new_data.csv --auth-list auth_list.csv --update-original
   # Then use the updated file for import
   import_tool --file reports/updated_file_*.csv
   ```

### Performance Optimization

For large datasets:

1. **Increase Process Pool**: Edit `duplicate_detection.py` to modify:

   ```python
   cpu_count = max(1, multiprocessing.cpu_count() - 1)
   ```
2. **Adjust Batch Size**: For memory-constrained environments, reduce:

   ```python
   batch_size = max(100, len(input_df) // (cpu_count * 2))
   ```
3. **Disable Advanced Matching**: For faster processing with very large datasets

---

## Troubleshooting

### Common Issues and Solutions

#### Application Won't Start

**Issue**: Python environment or dependency problems
**Solution**:

1. Verify Python installation: `python --version`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check for conflicting packages: `pip list`

#### File Loading Errors

**Issue**: CSV format or permission problems
**Solution**:

1. Verify CSV file format and encoding (UTF-8 recommended)
2. Check file permissions
3. Ensure the file isn't open in another application

#### Slow Performance

**Issue**: Large datasets or resource constraints
**Solution**:

1. Lower the matching threshold for faster processing
2. Disable advanced matching
3. Process data in smaller batches
4. Allocate more system resources

#### Unexpected Validation Results

**Issue**: Misunderstanding of validation rules
**Solution**:

1. Review the validation rules section in this manual
2. Check log files for detailed validation reasoning
3. Manually inspect a few examples to understand the pattern

### Log Files

Detailed logs are stored in the `logs` directory. The default log level is INFO, but you can set it to DEBUG for more detailed information:

```bash
python src/main.py --log-level DEBUG
```

---

## FAQ

### General Questions

**Q: How many entities can EVS process?**
A: EVS can handle datasets of up to 100,000 entities, though performance will depend on your hardware.

**Q: Can I customize the naming convention rules?**
A: Yes, rules can be customized by modifying the configuration files and, for advanced customization, by extending the Python code.

**Q: Does EVS modify my original files?**
A: No, EVS creates new files with the changes unless you specifically request to update the original file.

### Technical Questions

**Q: Which matching algorithm is best?**
A: The combined approach (default) typically provides the best results as it leverages multiple techniques.

**Q: How should I set the matching threshold?**
A: Start with the default (85%) and adjust based on your results. Increase for fewer false positives, decrease for fewer false negatives.

**Q: Can EVS handle non-English entity names?**
A: Yes, but phonetic matching works best with English names. Other matching techniques work well across languages.

**Q: Is GPU acceleration supported?**
A: When TensorFlow is installed with GPU support, the ML-based matching can utilize GPU acceleration.

---

## Glossary

**Authoritative Entity List**: The reference list of official entity names against which input data is validated.

**Entity**: A distinct business, organization, or institution identified by a name in the data.

**Fuzzy Matching**: Techniques to find similarities between strings that are not exactly identical.

**Levenshtein Distance**: A string metric measuring the difference between two sequences based on the minimum number of operations required to transform one into the other.

**Matching Threshold**: The minimum similarity score (0-1) required for two entities to be considered potential matches.

**Naming Convention**: A set of rules governing how entity names should be formatted for consistency.

**Phonetic Matching**: Matching based on how words sound rather than how they are spelled.

**Soundex**: A phonetic algorithm for indexing names by sound as pronounced in English.

**Token-Based Matching**: Comparing strings by breaking them into words or tokens, useful for catching reordered words.

**Validation Rule**: A specific criterion that entity names must meet to be considered valid.
