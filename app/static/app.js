const sourceName = document.querySelector("#sourceName");
const documentText = document.querySelector("#documentText");
const fileInput = document.querySelector("#fileInput");
const analyzeButton = document.querySelector("#analyzeButton");
const statusNode = document.querySelector("#status");
const summaryNode = document.querySelector("#summary");
const flagsNode = document.querySelector("#flags");
const jsonOutput = document.querySelector("#jsonOutput");

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;
  sourceName.value = file.name;
  documentText.value = await file.text();
});

analyzeButton.addEventListener("click", async () => {
  statusNode.textContent = "Analyzing";
  flagsNode.innerHTML = "";
  summaryNode.textContent = "";
  jsonOutput.textContent = "{}";

  const response = await fetch("/analyze/text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      source_name: sourceName.value || "pasted_text",
      text: documentText.value,
    }),
  });

  if (!response.ok) {
    statusNode.textContent = "Analysis failed";
    jsonOutput.textContent = await response.text();
    return;
  }

  const result = await response.json();
  statusNode.textContent = `Analysis #${result.id}`;
  summaryNode.textContent = result.summary;
  renderFlags(result.risk_flags);
  jsonOutput.textContent = JSON.stringify(result, null, 2);
});

function renderFlags(flags) {
  if (!flags.length) {
    flagsNode.innerHTML = '<div class="flag">No risk flags detected by the starter rules.</div>';
    return;
  }

  flags.forEach((flag) => {
    const item = document.createElement("article");
    item.className = `flag ${flag.severity}`;
    item.innerHTML = `
      <strong>${flag.severity}</strong> ${flag.flag_type.replaceAll("_", " ")}
      <p>${flag.explanation}</p>
      <p>${flag.suggested_review}</p>
    `;
    flagsNode.appendChild(item);
  });
}
