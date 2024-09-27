import os
import json
import random
import copy
import argparse
from config import alternative_fonts, all_string_bools, get_random_font, get_random_string_bool, get_random_locale
import webcolors
import re

# Transformation functions
def transform_boolean(value):
    """Invert the boolean value."""
    return [not value]

def transform_number(value):
    """Generate a list of unique transformations for numerical values."""
    transformations = set()
    if isinstance(value, (int, float)):
        # Basic transformations
        transformations.add(value * 2)  # Double the value
        transformations.add(value - 1)  # Subtract 1
        transformations.add(-value)     # Negate the value
        transformations.add(value + value * 0.1)   # Add 10% of the value
        transformations.add(value - value * 0.1)   # Subtract 10% of the value
        transformations.add(value + value * 1.0)   # Add 100% of the value
        transformations.add(value - value * 1.0)   # Subtract 100% of the value

    return list(transformations)

def transform_percentage(value):
    """Transform percentages by adding/subtracting 10% and 100%."""
    transformations = set()
    if isinstance(value, str) and re.match(r'^-?\d+(\.\d+)?%$', value):
        try:
            original_value = float(value[:-1])
            # Basic transformations: ±10% and ±100% of the percentage
            transformations.add(f"{original_value + original_value * 0.1}%")  # Add 10%
            transformations.add(f"{original_value - original_value * 0.1}%")  # Subtract 10%
            transformations.add(f"{original_value + original_value * 1.0}%")  # Add 100%
            transformations.add(f"{original_value - original_value * 1.0}%")  # Subtract 100%

        except ValueError:
            pass
    return list(transformations) if transformations else [value]

def transform_hex_color(value):
    """Randomly transform hex color strings."""
    transformations = set()
    if isinstance(value, str) and re.match(r'^#([A-Fa-f0-9]{6})$', value):
        try:
            # Reverse hex to color names, then choose a random color
            css3_names_to_hex = {v: k for k, v in webcolors.CSS3_HEX_TO_NAMES.items()}
            random_color_name = random.choice(list(css3_names_to_hex.keys()))
            transformations.add(webcolors.name_to_hex(random_color_name))
        except AttributeError:
            # Fallback if webcolors fails
            return [value]
    return list(transformations) if transformations else [value]

def transform_font(value):
    """Randomly change font family if it's in the predefined list of fonts."""
    transformations = set()
    if isinstance(value, str) and value.lower() in alternative_fonts:
        transformations.add(get_random_font())
    return list(transformations) if transformations else [value]

def transform_string(value):
    """Transform strings that represent boolean-like values."""
    transformations = set()
    
    # Check if the string is in the all_string_bools dictionary
    if isinstance(value, str) and value in all_string_bools:
        # Get the opposite boolean-like value from all_string_bools, e.g., No --> Yes
        transformations.add(all_string_bools[value])
    
    return list(transformations) if transformations else [value]


def transform_value(key, value):
    """Apply the appropriate transformation based on the value type."""
    if isinstance(value, bool):
        return transform_boolean(value)
    elif isinstance(value, (int, float)):
        return transform_number(value)
    elif isinstance(value, str):
        # Apply different string-related transformations
        transformed_values = set()
        transformed_values.update(transform_hex_color(value))
        transformed_values.update(transform_font(value))
        transformed_values.update(transform_string(value))
        transformed_values.update(transform_percentage(value))
        return list(transformed_values)
    else:
        return [value]  # No transformation for other types

# Apply combinatorial transformations and generate new JSON objects
def apply_combinatorial_transformations(data, output_dir):
    """Generate multiple variations of the input JSON by transforming values."""
    transformed_jsons = [data]  # Start with the original configuration

    def transform_dict(d, path=""):
        """Recursively transform dictionary values."""
        for key, value in d.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                # Recursively process nested dictionaries
                transform_dict(value, current_path)
            else:
                # Apply transformations to the value
                transformed_values = transform_value(key, value)
                if len(transformed_values) > 1:  # Only create new combinations if transformations exist
                    nonlocal transformed_jsons
                    new_transformed_jsons = []
                    for transform in transformed_values:
                        for transformed_json in transformed_jsons:
                            # Deep copy of the current JSON state
                            new_json = copy.deepcopy(transformed_json)
                            # Navigate to the correct path in the JSON object
                            keys = current_path.split(".")
                            sub_dict = new_json
                            for k in keys[:-1]:
                                sub_dict = sub_dict[k]
                            # Apply the transformation
                            sub_dict[keys[-1]] = transform
                            new_transformed_jsons.append(new_json)
                    # Ensure transformations are unique by serializing and then converting back to dict
                    transformed_jsons = [json.loads(t) for t in {json.dumps(d, sort_keys=True) for d in new_transformed_jsons}]
                else:
                    # If no transformation, retain the original value
                    for transformed_json in transformed_jsons:
                        keys = current_path.split(".")
                        sub_dict = transformed_json
                        for k in keys[:-1]:
                            sub_dict = sub_dict[k]
                        sub_dict[keys[-1]] = transformed_values[0]

    # Start transforming from the root level
    transform_dict(data)
    
    # Save each transformed JSON as a file
    for i, transformed_json in enumerate(transformed_jsons):
        print(f"Extracting configuration {i+1}...")  # Print extracting message
        output_filename = os.path.join(output_dir, f"config{i+1}.json")
        with open(output_filename, 'w') as outfile:
            json.dump(transformed_json, outfile, indent=2)
        print(f"Transformed JSON {i + 1} saved to {output_filename}")

    return transformed_jsons

# Main function to handle command-line arguments
def main(config_file):
    """Load the JSON file, apply transformations, and save the new configurations."""
    # Load JSON data from the configuration file
    with open(config_file, 'r') as file:
        data = json.load(file)

    # Create 'configurations' directory if it doesn't exist
    output_dir = 'configurations'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Apply combinatorial transformations and save each one
    apply_combinatorial_transformations(data, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simplified fuzzing in configurations.')
    parser.add_argument('config_file', type=str, help='Path to the configuration JSON file')
    args = parser.parse_args()

    main(args.config_file)
