# Harnessing Multiplicity Granular Browser Extension Fingerprinting through User Configurations - Artifacts Page

## Summary
Our paper introduces a technique for extracting multiple unique signatures from browser extensions by exploiting various user configuration options. We present results from various extensions and provide tools for testing and automation.

This page provides artifacts related to our paper, which introduces a technique for extracting multiple signatures from browser extensions by leveraging various user configuration options. We showcase extensions with varying configuration options and present the resulting signatures.

Additionally, we offer the necessary code for fuzzing, generating configuration options, and automating extension testing. Each configuration is applied through an additional  content script, and the corresponding signature is extracted.

Our main components are :
- Fuzzing: The technique used to generate various configurations for testing by  changing values in the options. The script reads an extension's options and generates multiple potential configurations.
- Multiple Signature extraction: The script that navigates through our controlled web page applies configurations and extracts the extension's fingerprints (signatures).

## Artifacts Details

We analyze and test the  following extensions:

| Name                               | ID                                | Options | Users |
|------------------------------------|-----------------------------------|---------|-------|
| `Color Temperature (Change Lux)`   | mppedbpcpkaeclkgoppmdpdobhlpifeb  | 5       | 5K    |
| `OpenDyslexic`                     | cdnapgfjopgaggbmfgbiinmmbdcglnam  | 2       | 700K  |
| `Dyslexia Friendly`                | miepjgfkkommhllbbjaedffcpkncboeo  | 4       | 10K   |
| `Dark Reader`                      | eimadpbcbfnmbkopoojfekhnkhdbieeh  | 20      | 5M    |


The `extensions` folder  is organized into directories corresponding to each extension, containing configuration options and different signatures.
For each extension folder, we include:
- **extensionID:** The original code extracted from the Chrome Web Store.
- `configuration.json`: The default configuration options for the extension.
- **Configurations Directory:**
  - `config1.json`, `config2.json`, `configX`: Various options specific to the extension.
- **Signatures Directory:**
  - Baseline signature: The fingerprint of the extension without customization.
  - Configuration-specific signatures: For each configuration (e.g., `config1.json`), there is a corresponding signature file (e.g., `signature1.json`).

### Honeypage

This directory contains a simplified version of our honeypage in HTML, and  a Node.js server to host the page locally.

### Fuzzing (Section 3: Methodology - Fuzzing)

This directory includes a simplified version of the options fuzzing component, targeting the majority of boolean, string, and numerical values.

### Signature Extraction (Section 5: Evaluation)

The folder `testing` contains the main logic of the configuration testing. It generates a new content-script that applies the options to the extension, and updates the `Manifest.json` automatically. The script then visits the honeypage and extracts the additional signatures.



### Testing  Configuration Fuzzing

1. **Install fuzzing and crawler requirements in the main directory:**
  ```sh
     pip install requirements.txt
  ```
  This will install Selenium and webcolors required for fuzzing and crawler script.



2. **Run  Fuzzing:**
   This script generates and stores multiple fuzzed configurations in the `configurations` folder for a given extension options object. 

      ```sh
      python fuzzing_options.py ../extensions/<extension-name>/configurations/configuration.json
      ```
  After running the fuzzing script, expect to see several new configuration files (e.g., `config1.json`, `config2.json`, etc.) in the `configurations` folder.
  **Example configurations:**

```json
// configuration.json
{
  "enabled": false,
  "font": "bold"
}
```
```json
// config1.json
{
  "enabled": true,
  "font": "italic"
}
```

### Extracting multiple signatures through configurations

1. **Set up the Honeypage:**

    - Navigate to the `honeypage` directory and install necessary Node.js packages (ensure Node.js and npm are installed)
      ```sh
      npm init -y
      npm install express --save  
      ```

    - Start the Node server:
      ```sh
      npm start
      ```

    The honeypage will be available at `http://localhost:3000`.

  
3. **Prepare Configuration Files:**
    The fuzzing component stores the configuration file(s) in the `configurations` directory for each extension. Each file represents a different set of options for the extension and can be used for the next step.


3. **Test and Extract Signatures:**

    - Crawler runs on top of Chrome browser using Selenium. Any version of Chrome with a suitable Selenium version will work. The latest versions are also recommended.

    - Run the crawler script with the configuration folder and the extension's code folder as arguments:
      ```sh
      python3 crawler.py <configurations_path> ../extensions/<extension-name>/<extensionID>
      ```

This process will launch a new browser instance, apply each configuration, and extract the signatures, which are then stored in the signatures directory. 
Each script runs once to generate the extension signatures for simplicity and verification.


5. **Testing with given options:**
You can directly test using the options provided in each extension folder <extension-name/configuration>:
 ```sh
python crawler.py ../extensions/darkreader/configurations/ ../extensions/darkreader/eimadpbcbfnmbkopoojfekhnkhdbieeh/
python crawler.py ../extensions/opendyslexic/configurations/ ../extensions/opendyslexic/cdnapgfjopgaggbmfgbiinmmbdcglnam/
python crawler.py ../extensions/dyslexiafriendly/configurations/ ../extensions/dyslexiafriendly/miepjgfkkommhllbbjaedffcpkncboeo/
python crawler.py ../extensions/color_temperature/configurations/ ../extensions/color_temperature/mppedbpcpkaeclkgoppmdpdobhlpifeb/
   ```

### Additional Notes
- Fuzzing and signature extraction can be tested independently, and various configurations are already included for testing.
- The crawler will not function in headless mode due to Chrome's restrictions on loading extensions.
- During signature extraction, click the extension button to verify that the options have been changed successfully.

