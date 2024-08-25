import os
import json
import random
import copy
import argparse
from config import alternative_fonts, all_string_bools, get_random_font, get_random_string_bool, get_random_locale
import webcolors

# Transformation functions
def transform_boolean(value):
    return [not value]

def transform_number(value):
    transformations = []
    if isinstance(value, (int, float)):
        transformations.append(value * 2)  # Double the value
        transformations.append(value - 1)  # Subtract 1
        transformations.append(-value)     # Negate the value
        # Add more transformations as needed
    return transformations

def transform_percentage(value):
    transformations = []
    if isinstance(value, str) and value.endswith("%"):
        original_value = float(value[:-1])
        transformations.append(f"{original_value + random.uniform(-5, 5)}%")
        transformations.append(f"{original_value + random.uniform(-10, 10)}%")
        # Add more transformations as needed
    return transformations if transformations else [value]

def transform_hex_color(value):
    if isinstance(value, str) and value.startswith("#") and len(value) == 7:
        # Fetch a random CSS3 color name and convert it to hex
        random_color_name = random.choice(list(webcolors.CSS3_NAMES_TO_HEX.keys()))
        return [webcolors.name_to_hex(random_color_name)]
    return [value]

def transform_font(value):
    if isinstance(value, str) and value.lower() in alternative_fonts:
        return [get_random_font()]
    return [value]

def transform_string(value):
    transformations = []
    if isinstance(value, str) and value.lower() in all_string_bools:
        transformations.append(all_string_bools[value.lower()])
        # Add more transformations as needed
    return transformations if transformations else [value]

def transform_value(key, value):
    if isinstance(value, bool):
        return transform_boolean(value)
    elif isinstance(value, (int, float)):
        return transform_number(value)
    elif isinstance(value, str):
        transformed_values = []
        transformed_values.extend(transform_hex_color(value))
        transformed_values.extend(transform_font(value))
        transformed_values.extend(transform_string(value))
        transformed_values.extend(transform_percentage(value))
        return transformed_values
    else:
        return [value]

# Apply combinatorial transformations and generate new JSON objects
def apply_combinatorial_transformations(data):
    transformed_jsons = [data]  # Start with the original configuration

    def transform_dict(d, path=""):
        for key, value in d.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                transform_dict(value, current_path)
            else:
                transformed_values = transform_value(key, value)
                if len(transformed_values) > 1:  # Apply combinatorial transformations
                    nonlocal transformed_jsons
                    new_transformed_jsons = []
                    for transform in transformed_values:
                        for transformed_json in transformed_jsons:
                            new_json = copy.deepcopy(transformed_json)
                            keys = current_path.split(".")
                            sub_dict = new_json
                            for k in keys[:-1]:
                                sub_dict = sub_dict[k]
                            sub_dict[keys[-1]] = transform
                            new_transformed_jsons.append(new_json)
                    transformed_jsons = new_transformed_jsons
                else:
                    for transformed_json in transformed_jsons:
                        keys = current_path.split(".")
                        sub_dict = transformed_json
                        for k in keys[:-1]:
                            sub_dict = sub_dict[k]
                        sub_dict[keys[-1]] = transformed_values[0]

    transform_dict(data)
    return transformed_jsons

# Main function to handle command-line arguments
def main(config_file):
    # Load JSON data from the configuration file
    with open(config_file, 'r') as file:
        data = json.load(file)

    # Apply combinatorial transformations
    transformed_jsons = apply_combinatorial_transformations(data)

    # Create 'configuration' directory if it doesn't exist
    output_dir = 'configurations'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Output the transformed JSON objects to separate files
    for i, transformed_json in enumerate(transformed_jsons):
        output_filename = os.path.join(output_dir, f"config{i+1}.json")
        with open(output_filename, 'w') as outfile:
            json.dump(transformed_json, outfile, indent=2)
        print(f"Transformed JSON {i + 1} saved to {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simplified fuzzing in configurations.')
    parser.add_argument('config_file', type=str, help='Path to the configuration JSON file')
    args = parser.parse_args()

    main(args.config_file)
