const form = document.getElementById("FileUploadForm");
const fileInput = document.getElementById("fileInput");
const modeSelect = document.getElementById("modeSelect");
const responseDiv = document.getElementById("response");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  if (!file) {
    alert("No file selected.");
    return;
  }

  const isPhoto = file.type.startsWith("image/");
  const formData = {
    is_photo: isPhoto,
    mode: modeSelect.value,
  };

  responseDiv.classList.remove("visible");
  responseDiv.style.display = "none";
  responseDiv.innerHTML = "Processing...";

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
    responseDiv.innerHTML = `<strong>Error:</strong> Could not read file.`;
    responseDiv.style.display = "block";
    setTimeout(() => {
      responseDiv.classList.add("visible");
    }, 10);
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
    responseDiv.innerHTML = `<strong>Error:</strong> An error occurred while processing your request.`;
  } finally {
    responseDiv.style.display = "block";
    setTimeout(() => {
      responseDiv.classList.add("visible");
    }, 10);
  }
}
