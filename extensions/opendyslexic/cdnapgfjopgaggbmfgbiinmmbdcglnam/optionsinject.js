
function updateOptions() {
    chrome.storage.local.set(
        {
    "enabled": true,
    "font": "italic"
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
