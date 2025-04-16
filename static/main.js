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
    }

    try {
        if (isPhoto) {
            const reader = new FileReader();
            reader.onload = async () => {
                formData.image = reader.result.split(",")[1]; // Base64 string
                console.log(reader.result.split(",")[1]);
                await sendData(formData);
            };
            reader.readAsDataURL(file); // THIS WAS MISSING
        } else {
            formData.text = await file.text();
            await sendData(formData);
        }
    } catch (error) {
        console.log(error);
        alert(error);
    }
});

async function sendData(formData) {
    try {
        const response = await fetch("/what", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }
        const data = await response.json();
        const responseDiv = document.getElementById("response");

        if (response.ok) {
            responseDiv.style.display = "block";
            responseDiv.innerHTML = `<strong>Response:</strong> ${data.response}`;
        } else {
            responseDiv.style.display = "block";
            responseDiv.innerHTML = `<strong>Error:</strong> ${data.error || "Unknown error"}`;
        }
    } catch (error) {
        console.log("Error:", error);
        alert("An error occurred while processing your request.");
    }
}