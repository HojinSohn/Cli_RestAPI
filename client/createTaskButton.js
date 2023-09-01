const titleInput = document.getElementById("titleInput");
const descriptionInput = document.getElementById("descriptionInput");
const timeInput = document.getElementById("datetimeDisplay");

function addNewTask() {
    const submitButton = document.querySelector(".submitButton");
    submitButton.innerText = "CREATE TASK";

    titleInput.value = ""
    titleInput.disabled = false
    descriptionInput.value = ""
    descriptionInput.disabled = false
    setDateTime(currentDate.toISOString());

    document.querySelector(".submitButton").onclick = createTaskAPI
}

const createTaskAPI = async () => {
    const response =  await fetch(`http://127.0.0.1:5000/task`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "title": titleInput.value,
            "description": descriptionInput.value,
            "timestamp": timeInput.value+":00",
        })
    });
    titleInput.value = ""
    descriptionInput.value = ""
    timeInput.value = ""
    location.reload();
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".addTaskButton").onclick = addNewTask;
});