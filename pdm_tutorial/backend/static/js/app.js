//=====================
// WAIT FOR DOM TO LOAD
//=====================

import { apiClient } from "./modules/api-client.js";

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");
  loadFiles();
});

async function loadFiles() {
  const fileListEl = document.getElementById("file-list");
  fileListEl.innerHTML = `<div class="loading"><p>Loading files...</p></div>`;

  try {
    const data = await apiClient.getFiles();
    displayFiles(data.files);
  } catch (error) {
    fileListEl.innerHTML = `<p style=color: var(--color-danger-500);">Error: ${error.message}</p>`;
  }
}

function displayFiles(files) {
  const container = document.getElementById("file-list");
  container.innerHTML = ""; // Clear teh loading message

  if (!files || files.length === 0) {
    container.innerHTML = "<p>No files found.</p>";
    return;
  }
  const fragment = document.createDocumentFragment();
  files.forEach((file) => {
    fragment.appendChild(createFileElement(file));
  });
  container.appendChild(fragment);
}

function createFileElement(file) {
  const div = document.createElement("div");
  div.className = "file-item";

  const infoDiv = document.createElement("div");
  infoDiv.className = "file-info";

  const nameSpan = document.createElement("span");
  nameSpan.className = "file-name";
  nameSpan.textContent = file.name;

  const statusSpan = document.createElement("span");
  statusSpan.className = `file-status status-${file.status}`;
  statusSpan.textContent = file.status.replace("_", " ");

  infoDiv.appendChild(nameSpan);
  infoDiv.appendChild(statusSpan);
  div.appendChild(infoDiv);
  return div;
}
