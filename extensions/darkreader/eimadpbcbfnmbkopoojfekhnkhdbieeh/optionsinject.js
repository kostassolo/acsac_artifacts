
function updateOptions() {
    chrome.storage.sync.set(
        {
    "automation": {
        "behavior": "OnOff",
        "enabled": false,
        "mode": ""
    },
    "changeBrowserTheme": false,
    "customThemes": [],
    "detectDarkTheme": false,
    "disabledFor": [],
    "displayedNews": [
        "thanks-2023"
    ],
    "enableContextMenus": false,
    "enableForPDF": true,
    "enableForProtectedPages": false,
    "enabled": true,
    "enabledByDefault": true,
    "enabledFor": [],
    "fetchNews": true,
    "location": {
        "latitude": null,
        "longitude": null
    },
    "presets": [],
    "previewNewDesign": false,
    "schemeVersion": 2,
    "syncSettings": true,
    "syncSitesFixes": false,
    "theme": {
        "brightness": 50,
        "contrast": 50,
        "darkColorScheme": "Default",
        "darkSchemeBackgroundColor": "#181a1b",
        "darkSchemeTextColor": "#e8e6e3",
        "engine": "dynamicTheme",
        "fontFamily": "Helvetica Neue",
        "grayscale": 0,
        "immediateModify": false,
        "lightColorScheme": "Default",
        "lightSchemeBackgroundColor": "#dcdad7",
        "lightSchemeTextColor": "#181a1b",
        "mode": 1,
        "scrollbarColor": "",
        "selectionColor": "auto",
        "sepia": 0,
        "styleSystemControls": false,
        "stylesheet": "",
        "textStroke": 0,
        "useFont": false
    },
    "time": {
        "activation": "18:00",
        "deactivation": "9:00"
    }
},
        function() {
            console.log('Options updated.');
        }
    );
}

// Main logic to execute when content script runs
async function main() {
    // Perform the update of options
    updateOptions();
}

// Run the main logic when content script is injected
main();
