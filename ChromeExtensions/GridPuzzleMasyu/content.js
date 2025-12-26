// content.js
// Injects the main world script

console.log("Masyu Solver Content Script Loaded");

function injectScript(file_path, tag) {
    var node = document.getElementsByTagName(tag)[0];
    var script = document.createElement('script');
    script.setAttribute('type', 'text/javascript');
    script.setAttribute('src', file_path);
    node.appendChild(script);
}

// Inject the loader script that has access to window
injectScript(chrome.runtime.getURL('inject.js'), 'body');

// Listen for messages from the injected script if needed
window.addEventListener("message", function(event) {
  if (event.source != window) return;
  if (event.data.type && (event.data.type == "FROM_PAGE")) {
    console.log("Content script received: " + event.data.text);
  }
});
