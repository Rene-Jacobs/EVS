"""
validation_rules.py

This module contains the rules for entity name validation according to the
specified naming convention standards.
"""

import re
import string


class ValidationRules:
    """Class containing validation rules and methods for entity names."""

    # Default configuration values
    DEFAULT_FUZZY_MATCH_THRESHOLD = 85

    # Business designations to remove
    BUSINESS_DESIGNATIONS = [
        "LLC",
        "Inc",
        "Inc.",
        "Incorporated",
        "Corp",
        "Corp.",
        "Corporation",
        "Ltd",
        "Ltd.",
        "Limited",
        "L.P.",
        "LP",
        "LLP",
        "PLLC",
        "P.C.",
        "L.L.C.",
        "L.L.P.",
        "P.L.L.C.",
    ]

    # Common abbreviations to expand
    ABBREVIATIONS = {
        "Co": "Company",
        "Co.": "Company",
        "Bros": "Brothers",
        "Bros.": "Brothers",
        "Mfg": "Manufacturing",
        "Mfg.": "Manufacturing",
        "Intl": "International",
        "Intl.": "International",
        "&": "and",
    }

    # Government entity patterns
    GOVT_ENTITY_PATTERNS = {
        "state": r"^State of ([A-Za-z ]+)$",
        "county": r"^County of ([A-Za-z ]+)( \([A-Z]{2}\))?$",
        "city": r"^(City|Town|Village|Borough) of ([A-Za-z ]+)( \([A-Z]{2}\))?$",
    }

    # US state abbreviations
    US_STATES = {
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
        "DC",
        "AS",
        "GU",
        "MP",
        "PR",
        "VI",
    }

    def __init__(self, fuzzy_threshold=None):
        """
        Initialize ValidationRules with configurable settings.

        Args:
            fuzzy_threshold (int, optional): Threshold for fuzzy matching (0-100).
                Defaults to DEFAULT_FUZZY_MATCH_THRESHOLD.
        """
        self.fuzzy_threshold = fuzzy_threshold or self.DEFAULT_FUZZY_MATCH_THRESHOLD

    def apply_all_rules(self, entity_name):
        """
        Apply all validation rules to an entity name.

        Args:
            entity_name (str): The entity name to validate.

        Returns:
            tuple: (validated_name, list of violations)
        """
        if not entity_name or not isinstance(entity_name, str):
            return "", ["Empty or invalid entity name"]

        violations = []

        # Track the original and current state for reporting
        original_name = entity_name
        current_name = entity_name

        # Rule 1: Check if it's using acronyms (hard to implement automatically)
        # This would require a database of known acronyms and their expansions

        # Rule 2: Replace ampersands
        if "&" in current_name:
            violations.append("Ampersand used instead of 'and'")
            current_name = self._replace_ampersands(current_name)

        # Rule 3: Remove apostrophes
        if "'" in current_name:
            violations.append("Apostrophes should be removed")
            current_name = self._remove_apostrophes(current_name)

        # Rule 4: Check for special characters (except parentheses in govt entities)
        is_govt_entity = self._is_government_entity(current_name)
        if not is_govt_entity and self._has_special_characters(current_name):
            violations.append("Special characters should be removed")
            current_name = self._remove_special_characters(current_name, is_govt_entity)

        # Rule 5: Remove business designations
        has_designation = self._has_business_designation(current_name)
        if has_designation:
            violations.append("Business designations should be removed")
            current_name = self._remove_business_designations(current_name)

        # Rule 6: Expand company abbreviations
        has_abbrev = self._has_abbreviation(current_name)
        if has_abbrev:
            violations.append("Abbreviations should be expanded")
            current_name = self._expand_abbreviations(current_name)

        # Rule 7: Official spellings (would require a database of correct spellings)
        # Not implemented as it requires specific knowledge

        # Rule 8: Government entity formatting
        govt_entity_issue = self._check_government_entity_format(current_name)
        if govt_entity_issue:
            violations.append(govt_entity_issue)
            current_name = self._format_government_entity(current_name)

        # Rule 9: Convert to title case
        if current_name != current_name.title():
            violations.append("Entity name should be in title case")
            current_name = current_name.title()

        # If no changes were made, clear the violations list
        if original_name == current_name:
            violations = []

        return current_name, violations

    def _replace_ampersands(self, name):
        """Replace '&' with 'and'."""
        return name.replace("&", "and")

    def _remove_apostrophes(self, name):
        """Remove apostrophes from the name."""
        return name.replace("'", "")

    def _has_special_characters(self, name):
        """Check if name contains special characters."""
        # Define characters to allow (alphanumeric, spaces, and parentheses for state codes)
        allowed_chars = set(string.ascii_letters + string.digits + " ()")
        return any(char not in allowed_chars for char in name)

    def _remove_special_characters(self, name, is_govt_entity=False):
        """
        Remove special characters from name.

        If is_govt_entity is True, preserve parentheses for state codes.
        """
        if is_govt_entity:
            # For government entities, keep parentheses for state codes
            # but remove other special characters
            pattern = r"[^\w\s\(\)]"
        else:
            # For non-government entities, remove all special characters
            pattern = r"[^\w\s]"

        return re.sub(pattern, "", name)

    def _has_business_designation(self, name):
        """Check if name contains business designations."""
        for designation in self.BUSINESS_DESIGNATIONS:
            # Match whole words only with word boundaries
            pattern = r"\b" + re.escape(designation) + r"\b"
            if re.search(pattern, name):
                return True
        return False

    def _remove_business_designations(self, name):
        """Remove business designations from name."""
        result = name
        for designation in self.BUSINESS_DESIGNATIONS:
            # Match whole words only with word boundaries
            pattern = r"\b" + re.escape(designation) + r"\b"
            result = re.sub(pattern, "", result).strip()
            # Remove any double spaces that might result
            result = re.sub(r"\s+", " ", result).strip()
        return result

    def _has_abbreviation(self, name):
        """Check if name contains known abbreviations."""
        for abbrev in self.ABBREVIATIONS:
            # Match whole words only with word boundaries
            pattern = r"\b" + re.escape(abbrev) + r"\b"
            if re.search(pattern, name):
                return True
        return False

    def _expand_abbreviations(self, name):
        """Expand abbreviations in name."""
        result = name
        for abbrev, expansion in self.ABBREVIATIONS.items():
            # Match whole words only with word boundaries
            pattern = r"\b" + re.escape(abbrev) + r"\b"
            result = re.sub(pattern, expansion, result)
        return result

    def _is_government_entity(self, name):
        """Check if name is a government entity."""
        for pattern in self.GOVT_ENTITY_PATTERNS.values():
            if re.match(pattern, name):
                return True

        # Check for state pattern
        if re.match(r"^State of [A-Za-z ]+$", name):
            return True

        return False

    def _check_government_entity_format(self, name):
        """
        Check if government entity name follows the correct format.
        Returns an error message if format is incorrect, None otherwise.
        """
        # Check for county format
        county_match = re.match(r"^County of ([A-Za-z ]+)( \([A-Z]{2}\))?$", name)
        if county_match and not county_match.group(2):
            return "County must include state in parentheses"

        # Check for city/town format
        city_match = re.match(
            r"^(City|Town|Village|Borough) of ([A-Za-z ]+)( \([A-Z]{2}\))?$", name
        )
        if city_match and not city_match.group(3):
            return f"{city_match.group(1)} must include state in parentheses"

        # Check for state code validity
        state_code_match = re.search(r"\(([A-Z]{2})\)", name)
        if state_code_match and state_code_match.group(1) not in self.US_STATES:
            return f"Invalid state code: {state_code_match.group(1)}"

        return None

    def _format_government_entity(self, name):
        """Format government entity according to rules."""
        # This is a placeholder for more complex formatting logic
        # In a real-world application, this would need more detailed implementation
        # based on the specific requirements for each type of government entity
        return name

    def set_fuzzy_threshold(self, threshold):
        """
        Set the fuzzy matching threshold.

        Args:
            threshold (int): Value between 0 and 100.

        Raises:
            ValueError: If threshold is not between 0 and 100.
        """
        if not 0 <= threshold <= 100:
            raise ValueError("Fuzzy matching threshold must be between 0 and 100")
        self.fuzzy_threshold = threshold

    def get_fuzzy_threshold(self):
        """Get the current fuzzy matching threshold."""
        return self.fuzzy_threshold

