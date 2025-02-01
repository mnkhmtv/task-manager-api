const API_URL = "http://127.0.0.1:8000"; 

document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    
    document.getElementById("taskForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        const title = document.getElementById("title").value.trim();
        const description = document.getElementById("description").value.trim();

        if (!title || !description) {
            alert("Введите название и описание задачи!");
            return;
        }

        try {
            const response = await fetch(`${API_URL}/tasks`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, description })
            });

            if (!response.ok) {
                throw new Error(`Ошибка при добавлении задачи: ${response.statusText}`);
            }

            document.getElementById("taskForm").reset();
            loadTasks(); 
        } catch (error) {
            console.error(error);
            alert("Ошибка при добавлении задачи.");
        }
    });
});

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        if (!response.ok) throw new Error("Ошибка загрузки задач!");

        const tasks = await response.json();
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";
    
        tasks.forEach(task => {
            const li = document.createElement("li");
            li.innerHTML = `
                <strong>${task.title}</strong>: ${task.description}
                <button onclick="deleteTask('${task.id}')">Удалить</button>
            `;
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error(error);
        alert("Ошибка при загрузке задач.");
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, { method: "DELETE" });
        if (!response.ok) throw new Error("Ошибка при удалении задачи!");

        loadTasks();
    } catch (error) {
        console.error(error);
        alert("Не удалось удалить задачу.");
    }
}