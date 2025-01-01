import yaml
import re
import sys

def validate_footnotes(file_path):
    """
    Validate that all footnotes in sso_pricing lines have matching definitions.

    Args:
        file_path (str): Path to the YAML file to validate.

    Returns:
        list: List of validation errors.
    """
    errors = []
    footnotes = {}
    sso_pricing_footnotes = set()

    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Extract footnotes from footnotes entries
    for entry in data:
        if 'footnotes' in entry:
            match = re.match(r'\[\^([^]]+)\] (.*)', entry['footnotes'])
            if match:
                footnote_name = match.group(1)
                footnotes[footnote_name] = match.group(2)

    # Extract footnotes from sso_pricing entries
    for entry in data:
        if 'sso_pricing' in entry:
            match = re.search(r'\[\^([^]]+)\]', entry['sso_pricing'])
            if match:
                sso_pricing_footnote = match.group(1)
                sso_pricing_footnotes.add(sso_pricing_footnote)

    # Check for footnotes without definitions
    for footnote in sso_pricing_footnotes:
        if footnote not in footnotes:
            errors.append(f"Footnote '{footnote}' in sso_pricing entry has no definition.")

    # Check for definitions without footnotes
    for footnote in footnotes:
        if footnote not in sso_pricing_footnotes:
            errors.append(f"Footnote '{footnote}' has a definition but is not used in any sso_pricing entry.")

    if errors:
        raise ValueError("Validation errors:\n" + "\n".join(errors))

if __name__ == "__main__":
    try:
        validate_footnotes(sys.argv[1])
        print("No validation errors found.")
    except ValueError as e:
        print(f"Found Validation Errors: {e}")
        sys.exit(1)
