import os
import json
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

# Website to visit for extracting mutations
website = "http://127.0.0.1:3000"

# Directory to save the signature files
signatures_path = 'signatures'


# Helper function to convert Python objects to JavaScript-compatible objects
def python_to_js(obj):
    if isinstance(obj, dict):
        return {k: python_to_js(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [python_to_js(v) for v in obj]
    elif obj is True:
        return True
    elif obj is False:
        return False
    elif obj is None:
        return None
    else:
        return obj

# Generate JavaScript code to inject extension options via `chrome.storage`
def generate_options_script(options, extension_id):
    # Convert the options dictionary into JavaScript code
    options_code = json.dumps(options, indent=4)
    
    # Decide whether to use local or sync storage based on the extension ID
    storage_area = 'local'
    if "darkreader"   in extension_id or "dyslexia" in extension_id:
        storage_area = 'sync'

    # JavaScript code to inject the options into chrome.storage
    js_code = f'''
function updateOptions() {{
    chrome.storage.{storage_area}.set(
        {options_code},
        function() {{
            console.log('Options updated.');
        }}
    );
}}

// Main logic to execute when the content script runs
async function main() {{
    // Perform the update of options
    updateOptions();
}}

// Run the main logic when content script is injected
main();
'''

    return js_code

# Write the generated JavaScript code to a file inside the extension directory
def write_to_file(js_code, extension_path):
    with open(os.path.join(extension_path, 'optionsinject.js'), 'w') as f:
        f.write(js_code)
    print('optionsinject.js file generated successfully.')

# Update the extension by injecting options and modifying the manifest file
def update_extension(config_name, extension_path):
    try:
        # Load the extension options from the specified config file
        with open(config_name, 'r') as file:
            options_data = json.load(file)

        #Convert the options data to a JavaScript-compatible format
        js_options_data = python_to_js(options_data)

        # Generate the JavaScript code for injecting options
        js_code = generate_options_script(js_options_data, extension_path)

        # Write the JavaScript code to the extension directory
        write_to_file(js_code, extension_path)

        # Path to the manifest.json file inside the extension
        manifest_path = os.path.join(extension_path, 'manifest.json')

        # Load the manifest.json file
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Ensure content_scripts exists and add optionsinject.js if not already present
        if 'content_scripts' in manifest and len(manifest['content_scripts']) > 0:
            if 'optionsinject.js' not in manifest['content_scripts'][0].get('js', []):
                manifest['content_scripts'][0]['js'].append('optionsinject.js')
        else:
            # Create the content_scripts section if it doesn't exist
            manifest['content_scripts'] = [{
                "matches": ["<all_urls>"],
                "js": ["optionsinject.js"],
                "run_at": "document_start",
                "all_frames": True,
                "match_about_blank": True
            }]

        # Write the updated manifest back to the manifest.json file
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)

        print(f'Manifest updated successfully for {config_name}.')

    except Exception as exc:
        print(f"An error occurred while updating extension for {config_name}: {exc}")

# Visit the website and extract mutations using the injected extension
def visit(driver, website, config_name, config_number):
    try:
        # Visit the target website
        driver.get(website)
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(8)  # Allow the extension to initialize itself
        driver.get(website)
        driver.switch_to.window(driver.window_handles[0])

        driver.switch_to.window(driver.window_handles[0])

        time.sleep(8)

        # Extract mutation data from the extension
        res_list = driver.execute_script("return myMutations;")
        parsed_data = []
        for item in res_list:
            try:
                parsed_json = json.loads(item)  # Parse each mutation JSON object string
                parsed_data.append(parsed_json)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object: {e}")

        # Filter relevant mutation data
        filtered_data = []
        for entry in parsed_data:
            if entry['type'] == 'childList' and ('added' in entry or 'removed' in entry):
                filtered_data.append(entry)
            elif entry['type'] == 'attributes':
                filtered_data.append(entry)

        # Enumerate the filtered data
        enumerated_result = [{"mutation": i + 1, **item} for i, item in enumerate(filtered_data)]

        # Convert the enumerated result into JSON format
        json_data = json.dumps(enumerated_result, indent=4)

        if not os.path.exists(signatures_path):
            os.makedirs(signatures_path)

        # Save the filtered data to a file, matching the input config index (e.g., config1 -> signature1.json)
        output_file_name = f"signature{config_number}.json"
        file_path = os.path.join(signatures_path, output_file_name)

        # Write JSON data to the output file
        with open(file_path, "w+") as f:
            f.write(json_data)

        print(f"Signature extracted and saved to {file_path}")

    except Exception as e:
        print(f"Error extracting mutations for {config_name}: {e}")

# Main function to iterate through configurations, inject them, and extract signatures
def main(config_folder, extension_path, website):
    # Chrome options setup
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-pipe')
    options.add_experimental_option('extensionLoadTimeout', 60000)
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"--load-extension={extension_path}")

    try:
        # Iterate through each JSON configuration file in the config folder
        for index, filename in enumerate(os.listdir(config_folder)):
            if filename.endswith('.json'):
                config_path = os.path.join(config_folder, filename)
                match = re.search(r'config(\d+)\.json', filename)
                config_number = match.group(1)  # Extract the number from the config filename

                # Update the extension with the current configuration
                update_extension(config_path, extension_path)

                # Initialize the Chrome WebDriver
                driver = webdriver.Chrome(options=options)

                # Visit the website and extract mutation signatures
                visit(driver, website, filename.split('.')[0], config_number)

                # Quit the driver to release resources
                if 'driver' in locals():
                    driver.quit()

                time.sleep(5)  # Adjust sleep time as needed

    except Exception as exc:
        print(f"An error occurred: {exc}")

    finally:
        if 'driver' in locals():
            driver.quit()

# Entry point for the script
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extension option inject and signature extraction from honeypage.")
    parser.add_argument("config_folder", help="Path to folder containing configuration JSON files")
    parser.add_argument("extension_path", help="Path to extension directory")
    args = parser.parse_args()

    # Call the main function with the provided arguments
    main(args.config_folder, args.extension_path, website)
