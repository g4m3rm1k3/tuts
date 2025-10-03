// This function will run when the entire HTML document has been loaded.
document.addEventListener("DOMContentLoaded", () => {
  // We immediately call our main function to fetch and display the files.
  loadFiles();
  debugLoadFiles();
});

// This is an async function because fetching data over a network takes time.
async function loadFiles() {
  try {
    // 1. "fetch" the data from our new API endpoint.
    const response = await fetch("/api/files");
    // 2. Convert the raw resopnse into JSON format.
    const files = await response.json();
    // 3. Pass the data to another function to handle displaying it.
    renderFiles(files);
  } catch (error) {
    // A simple way to handle errors if the server is down.
    console.error("Failed to load files:", error);
    const fileListContainer = document.getElmenetById("file-list");
    fileListContainer.innerHTML =
      "<p>Error loading files. Is the server running?</p>";
  }
}

function renderFiles(files) {
  // 1. Get the HTML element whre we want to display our list
  const fileListContainer = document.getElementById("file-list");

  // 2. Clear out any old content (liek a "loading..." message).
  fileListContainer.innerHTML = "";

  // 3. Loop through each file object in the data array.
  files.forEach((file) => {
    // 4. For each file, create a new paragraph element as a string.
    const fileElement = `<p>${file.name} - Status: ${file.status}</p>`;
    // 5. Add this new HTML string to our container.
    fileListContainer.innerHTML += fileElement;
  });
}

async function debugLoadFiles() {
  console.log("[1] Starting load");

  const response = await fetch("/api/files");
  console.log("[2] Got reponse:", response.status);

  const data = await response.json();
  console.log("[3] Parsed JSON:", data.length, "items");

  document.getElementById("file-list").innerHTML = "";
  data.forEach((file) => {
    const elem = document.createElement("div");
    elem.textContent = file.name;
    document.getElementById("file-list").appendChild(elem);
  });
  console.log("[4] DOM updated");
}
