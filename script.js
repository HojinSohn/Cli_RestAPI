const currentDate = new Date();

const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];
console.log(currentDate)
const currentMonth = months[currentDate.getMonth()];
const currentYear = currentDate.getFullYear();
const currentDateDate = currentDate.getDate();

const monthYearElement = document.getElementById('currentDate');
monthYearElement.textContent = `${currentMonth}  ${currentDateDate}  ${currentYear}`;

const taskStates = {};

const getTaskList = async () => {
    const response = await fetch('http://127.0.0.1:5000/task');
    const taskJsons = await response.json();
    const taskList = taskJsons.map(taskJson => {
        const taskDate = new Date(taskJson.timestamp)
        const timeDifference = taskDate - currentDate;

        const daysDiff = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        // const hoursDiff = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        return`
            <div class="taskDisplay" id="${taskJson.title}u" style="display: none">
                <button class="taskButton" data-task='${JSON.stringify(taskJson)}'>
                    <div class="taskCard">
                      <div class="taskCard-title">${taskJson.title}</div>
                      <div class="taskCard-description">${taskJson.description}</div>
                      <div class="taskCard-time">${new Date(taskJson.timestamp)}</div>
                    </div>
                    ${
                        daysDiff > 0 ?
                            `<p>${daysDiff} day left</p>`
                            // : hoursDiff < 0 
                            //     ? `<p>${hoursDiff} hours left</p>`
                            : `<p>overdue</p>`
                    }
                </button>
                <div class="manageButtonContainer">
                    <button class="taskHandleButton" id="update" onclick="updateTask(${taskJson.id})">UPDATE</button>
                    <button class="taskHandleButton" id="delete" onclick="deleteTask(${taskJson.id})">Delete</button>
                </div>
            </div> 
            
            <div class="taskDisplay" id="${taskJson.title}o">
                    <button class="taskButton" data-task='${JSON.stringify(taskJson)}'>
                        <p class="timestamp">${new Date(taskJson.timestamp)}</p>
                        <span>${taskJson.title}</span>
                    </button> ${
                        daysDiff > 0 ?
                            `<p>${daysDiff} day left</p>`
                            // : hoursDiff < 0 
                            //     ? `<p>${hoursDiff} hours left</p>`
                            : `<p>overdue</p>`
                    }
            </div>`;
    });


    const listContainer = document.getElementById("list");
    listContainer.innerHTML = taskList.join('<br>');

    // Attach event listener to the parent list container
    listContainer.addEventListener("click", function(event) {
        const clickedButton = event.target.closest(".taskButton");
        if (clickedButton) {
            const taskJson = JSON.parse(clickedButton.dataset.task);
            toggleContent(taskJson.title);
        }
    });
}



function toggleContent(title) {
    const originalContent = document.getElementById(`${title}o`);
    const updatedContent = document.getElementById(`${title}u`);

    // Toggle the visibility of original and updated content
    if (taskStates[title] === "updated") {
        originalContent.style.display = "flex";
        updatedContent.style.display = "none";
        taskStates[title] = "original";
    } else {
        originalContent.style.display = "none";
        updatedContent.style.display = "flex";
        taskStates[title] = "updated";
    }
}

async function updateTask(taskID) {
    document.querySelector(".submitButton").innerText = "UPDATE TASK"
    const response = await fetch(`http://127.0.0.1:5000/task/${taskID}`);
    const taskJson = await response.json();
    const titleInput = document.getElementById("titleInput");
    const descriptionInput = document.getElementById("descriptionInput");
    titleInput.disabled = false;
    descriptionInput.disabled = false;
    titleInput.value = taskJson.title
    descriptionInput.value = taskJson.description
    setDateTime((new Date(taskJson.timestamp)).toISOString());
    const updateTaskAPI = async () => {
        const response =  await fetch(`http://127.0.0.1:5000/task/${taskID}`, {
            method: "PUT",
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
    document.querySelector(".submitButton").onclick = () => {
        updateTaskAPI()
    }
}

async function deleteTask(taskID) {
    document.querySelector(".submitButton").innerText = "DELETE TASK"
    const response = await fetch(`http://127.0.0.1:5000/task/${taskID}`);
    const taskJson = await response.json();
    const titleInput = document.getElementById("titleInput");
    const descriptionInput = document.getElementById("descriptionInput");
    titleInput.disabled = true;
    descriptionInput.disabled = true;
    titleInput.value = taskJson.title
    descriptionInput.value = taskJson.description
    setDateTime((new Date(taskJson.timestamp)).toISOString());

    const deleteTask = async () => {
        const response =  await fetch(`http://127.0.0.1:5000/task/${taskID}`, {
            method: "DELETE",
        });
        titleInput.value = ""
        descriptionInput.value = ""
        location.reload();
    }

    document.querySelector(".submitButton").onclick = () => {
        deleteTask();
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await getTaskList();
});
