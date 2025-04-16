const form = document.getElementById("FileUploadForm");
const fileInput = document.getElementById("fileInput");
const modeSelect = document.getElementById("modeSelect");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  if (!file) {
    alert("No file.");
    return;
  }

  const isPhoto = file.type.startsWith("image/");
  const formData = {
    is_photo: isPhoto,
    mode: modeSelect.value,
  };

  try {
    if (isPhoto) {
      const base64 = await readFileAsBase64(file);
      formData.image = base64;
    } else {
      formData.text = await file.text();
    }

    await sendData(formData);
  } catch (error) {
    console.error(error);
    alert("An error occurred.");
  }
});

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = reader.result.split(",")[1];
      resolve(base64String);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function sendData(formData) {
  try {
    const response = await fetch("/what", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const responseDiv = document.getElementById("response");
    responseDiv.style.display = "block";

    const data = await response.json();

    if (response.ok) {
      responseDiv.innerHTML = `<strong>Response:</strong> ${data.response}`;
    } else {
      responseDiv.innerHTML = `<strong>Error:</strong> ${
        data.error || "Unknown error"
      }`;
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while processing your request.");
  }
}
