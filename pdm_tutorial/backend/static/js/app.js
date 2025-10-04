//=====================
// WAIT FOR DOM TO LOAD
//=====================

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");
  loadFiles();

  // Add event listener to refresh button
  const refreshBtn = document.getElementById("refresh-btn");
  refreshBtn.addEventListener("click", function () {
    console.log("Refresh button clicked");
    loadFiles();
  });
});

//LOAD FILES FROM API

async function loadFiles() {
  console.log("Loading files from API...");
  try {
    // Make GET reqeust to our API
    const response = await fetch("/api/files");

    // Check if request succeeded
    if (!response.ok) {
      throw new Error(`HTTP error! stastus: ${response.status}`);
    }

    // Parse JSON response
    const data = await response.json();
    console.log("Recieved dasta: ", data);

    // Display files
    displayFiles(data.files);
  } catch (error) {
    console.error("Error loading files: ", error);
    displayError("Failed to load files. Please refresh the page.");
  }
}

// Display Files in the DOM
function displayFiles(files) {
  // Find the container element
  const container = document.getElementById("file-list");

  // Clear loading message
  container.innerHTML = "";

  // Check if we have files
  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files found.</p>";
    return;
  }

  // Create HTML for each file
  files.forEach((file) => {
    const fileElement = createFileElement(file);
    container.appendChild(fileElement);
  });
  console.log(`Displayed ${files.length} files`);
}

// Create a single file element

function createFileElement(file) {
  // Create the container div
  const div = document.createElement("div");
  div.className = "file-item";

  // Create tfile name span
  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  // Create status span
  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  // Assemble the pisces
  div.appendChild(nameSpan);
  div.appendChild(statusSpan);

  return div;
}

// Display Error Mesage
function displayError(message) {
  const container = document.getElementById("file-list");
  container.innerHTML = `
    <div  style="color: red; padding: 1rem; background #fee; border-radius: 4px;">
    ${message}
    </div>`;
}
