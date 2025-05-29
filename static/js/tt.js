document.addEventListener("DOMContentLoaded", function () {
    const ttForm = document.getElementById("ttForm");
  
    if (ttForm) {
      ttForm.addEventListener("submit", async function (e) {
        e.preventDefault();
  
        const inputText = document.getElementById("input_text").value;
        const selectedOption = document.getElementById("options").value;
  
        const formData = new FormData();
        formData.append("input_text", inputText);
        formData.append("selected_option", selectedOption);
  
        try {
          const response = await fetch("/submit-tt-type", {
            method: "POST",
            body: formData
          });
  
          const data = await response.json();
  
          const resultSection = document.getElementById("tt-result");
          if (resultSection) {
            resultSection.innerHTML = "<h2>Decoded TT:</h2><ul style='list-style-type:none;'>" +
              data.result.map(line => `<li>${line}</li>`).join('') +
              "</ul>";
          }
        } catch (error) {
          console.error("Error submitting TT type:", error);
        }
      });
    }
  });
  