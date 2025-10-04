// This function will run when the entire HTML document has been loaded.
document.addEventListener("DOMContentLoaded", () => {
  // We immediately call our main function to fetch and display the files.
  loadFiles();
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
  fileListContainer.innerHTML = ""; // Clear previous content

  if (files.length === 0) {
    filesListContainer.innerHTML = "<p>No Cam files found in repository</p>";
  }

  // 3. Loop through each file object in the data array.
  files.forEach((file) => {
    // Use template literals (`) to biuld a more complex HTML sgtring
    const fileElementHTML = `
        <div class="file-item">
        <span class="file-name">${file.name}</span>
        <span class="status status-${file.status}">${file.status.replace(
      "_",
      " "
    )}</span>
        </div>
        `;
    // Use insertAdjacentHTML which is slightly more efficient than innerHTML +=
    fileListContainer.insertAdjacentHTML("beforeend", fileElementHTML);
  });
}

// Test innerHTML vs DocumentFragment
function testPerformance() {
  const testData = Array(1000)
    .fill()
    .map((_, i) => ({ name: `Files${i}` }));

  // Method 1: innerHTML
  console.time("innerHTML");
  let html = "";
  testData.forEach((file) => {
    html += `<div>${file.name}</div>`;
  });
  document.getElementById("test1").innerHTML = html;
  console.timeEnd("innerHTML");

  // Method 2: DocumentFragment
  console.time("fragment");
  const fragment = document.createDocumentFragment();
  testData.forEach((file) => {
    const div = document.createElement("div");
    div.textContent = file.name;
    fragment.appendChild(div);
  });
  document.getElementById("test2").appendChild(fragment);
  console.timeEnd("fragment");
}
