import os
import json
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
website="http://127.0.0.1:3000"
signatures_path = 'signatures'


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

def generate_options_script(options,extension_id):

    # Construct the JavaScript code for chrome.storage.sync.set()
    options_code = json.dumps(options, indent=4)
    storage_area='local'
    if "darkreader" in extension_id:
        storage_area= 'sync'
    js_code = f'''
function updateOptions() {{
    chrome.storage.{storage_area}.set(
        {options_code},
        function() {{
            console.log('Options updated.');
        }}
    );
}}

// Main logic to execute when content script runs
async function main() {{
    // Perform the update of options
    updateOptions();
}}

// Run the main logic when content script is injected
main();
'''

    return js_code

def write_to_file(js_code, extension_path):
    with open(os.path.join(extension_path, 'optionsinject.js'), 'w') as f:
        f.write(js_code)
    print('optionsinject.js file generated successfully.')

def update_extension(config_name, extension_path):
    try:
        # Load options data from the config file
        with open(config_name, 'r') as file:
            options_data = json.load(file)

        # Convert options_data to a JavaScript-friendly format
        js_options_data = python_to_js(options_data)

        # Generate the JavaScript code for optionsinject.js
        js_code = generate_options_script(js_options_data,extension_path)

        # Write the JavaScript code to optionsinject.js
        write_to_file(js_code, extension_path)

        # Path to manifest.json
        manifest_path = os.path.join(extension_path, 'manifest.json')

        # Load manifest.json
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Ensure content_scripts section exists and add optionsinject.js if not already present
        if 'content_scripts' in manifest and len(manifest['content_scripts']) > 0:
            if 'optionsinject.js' not in manifest['content_scripts'][0].get('js', []):
                manifest['content_scripts'][0]['js'].append('optionsinject.js')
        else:
            # If content_scripts section doesn't exist or is empty, create it with the injection
            manifest['content_scripts'] = [{
                "matches": ["<all_urls>"],
                "js": ["optionsinject.js"],
                "run_at": "document_start",
                "all_frames": True,
                "match_about_blank": True
            }]

        # Write updated manifest back to manifest.json
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)

        print(f'Manifest updated successfully for {config_name}.')

    except Exception as exc:
        print(f"An error occurred while updating extension for {config_name}: {exc}")

def visit(driver, website, config_name,index,config_number):
    try:
        # Visit the website
        driver.get(website)
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(8)  # Let extension initiate itself
        driver.get(website)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(8)
        # Extract mutations
        
        res_list = driver.execute_script("return myMutations;")
        parsed_data = []
        for item in res_list:
            try:
                parsed_json = json.loads(item)  # Parse each JSON object string
                parsed_data.append(parsed_json)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object: {e}")

        # Filter parsed data and generate signature
        filtered_data = []
        for entry in parsed_data:
            if entry['type'] == 'childList' and ('added' in entry or 'removed' in entry) or not 'added' in entry and not 'removed' in entry:
                filtered_data.append(entry)
            elif entry['type'] == 'attributes':
                filtered_data.append(entry)

        # Enumerate filtered data
        enumerated_result = [{"mutation": i + 1, **item} for i, item in enumerate(filtered_data)]

        # Convert enumerated result into JSON format
        json_data = json.dumps(enumerated_result, indent=4)

        if not os.path.exists(signatures_path):
            os.makedirs(signatures_path)

        file_path = os.path.join(signatures_path, f'signature{index}.json')


        # Write JSON data to a file
        with open(file_path, "w+") as f:
            f.write(json_data)

        print(f"Signature extracted and saved to {file_path}")

    except Exception as e:
        print(f"Error extracting mutations for {config_name}: {e}")

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
        # Iterate through each file in the config_folder
        for index, filename in enumerate(os.listdir(config_folder)):
            if filename.endswith('.json'):
                config_path = os.path.join(config_folder, filename)
                match = re.search(r'config(\d+)\.json', filename)
                config_number = match.group(1)
                # Update extension for the current configuration
                update_extension(config_path, extension_path)
                driver = webdriver.Chrome(options=options)

                # Visit website and extract signature
                visit(driver, website, filename.split('.')[0],index,config_number)

                # Quit the driver
                if 'driver' in locals():
                    driver.quit()

                time.sleep(5)  # Adjust as needed between iterations

    except Exception as exc:
        print(f"An error occurred: {exc}")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extension option inject and signature extraction from honeypage.")
    parser.add_argument("config_folder", help="Path to folder containing configuration JSON files")
    parser.add_argument("extension_path", help="Path to extension directory")
    args = parser.parse_args()

    # Call main function with command-line arguments
    main(args.config_folder, args.extension_path,website)
