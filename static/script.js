function extract() {
    const note = document.getElementById("clinical_note").value.trim();
    const fileInput = document.getElementById("file_input").files[0];
    const output = document.getElementById("output");
    const loading = document.getElementById("loading");
    const buttonsContainer = document.getElementById("buttons_container");

    output.innerText = "";
    buttonsContainer.classList.add("hidden"); // Hide buttons initially
    loading.classList.remove("hidden");

    let fetchOptions = { method: "POST" };

    // Determine Input Type
    if (fileInput) {
        const formData = new FormData();
        formData.append("file", fileInput);
        fetchOptions.body = formData;
    } else if (note) {
        fetchOptions.headers = { "Content-Type": "application/json" };
        fetchOptions.body = JSON.stringify({ text: note });
    } else {
        alert("Please enter text or upload a PDF.");
        loading.classList.add("hidden");
        return;
    }

    // Call for extraction on input
    fetch("/extract", fetchOptions)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                output.innerText = "Error extracting data.";
                buttonsContainer.classList.add("hidden");
            } else {
                output.innerText = JSON.stringify(data, null, 2);
                buttonsContainer.classList.remove("hidden"); // Show buttons when data is valid
            }
            loading.classList.add("hidden");
        })
        .catch(error => {
            output.innerText = "Error extracting data.";
            buttonsContainer.classList.add("hidden");
            loading.classList.add("hidden");
        });
}

// Copy output text to clipboard
function copyToClipboard() {
    const output = document.getElementById("output").innerText;
    if (!output) {
        alert("No extracted data to copy.");
        return;
    }
    navigator.clipboard.writeText(output).then(() => {
        alert("Copied to clipboard!");
    }).catch(err => {
        alert("Failed to copy: " + err);
    });
}

// Download output text as a JSON
function downloadJSON() {
    const output = document.getElementById("output").innerText;
    if (!output) {
        alert("No extracted data to download.");
        return;
    }
    const blob = new Blob([output], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "extracted_data.json";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}