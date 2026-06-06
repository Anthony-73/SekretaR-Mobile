function getDeviceId() {
    if (window.SekretaRAuth && typeof window.SekretaRAuth.getDeviceId === "function") {
        return window.SekretaRAuth.getDeviceId();
    }

    let deviceId = localStorage.getItem("device_id");

    if (!deviceId) {
        deviceId = crypto.randomUUID();
        localStorage.setItem("device_id", deviceId);
    }

    return deviceId;
}

function getUserId() {
    if (window.SekretaRAuth && typeof window.SekretaRAuth.getUserId === "function") {
        return window.SekretaRAuth.getUserId();
    }

    let userId = localStorage.getItem("user_id");

    if (!userId) {
        userId = crypto.randomUUID();
        localStorage.setItem("user_id", userId);
    }

    return userId;
}

function getAuthHeaders() {
    return {
        "device-id": getDeviceId(),
        "user-id": getUserId()
    };
}

function isTaskFilled(row) {
    const text = row.querySelector(".task-name-input")?.value?.trim() || "";
    const date = row.querySelector(".task-date-input")?.value?.trim() || "";
    const user = row.querySelector(".task-user-input")?.value?.trim() || "";
    return text && date && user;
}

function updateTaskRowState(row) {
    if (isTaskFilled(row)) {
        row.classList.add("green");
    } else {
        row.classList.remove("green");
    }
}

function normalizeExistingTaskRows() {
    const taskRows = document.querySelectorAll(".task-row");

    taskRows.forEach(row => {
        const nameEl = row.querySelector(".task-name");
        const dateEl = row.querySelector(".task-date");
        const userEl = row.querySelector(".task-user");
        const removeEl = row.querySelector(".task-remove");

        const oldDate = dateEl?.innerText?.trim() || "";
        const oldUser = userEl?.innerText?.trim() || "";
        const oldName = nameEl?.innerText?.trim() || "";

        if (nameEl && !nameEl.querySelector("input")) {
            const value = oldName && oldName !== "Задача появится после обработки файла" ? oldName : "";
            nameEl.innerHTML = `<input class="task-name-input" type="text" placeholder="Задача появится после обработки файла" value="${value}">`;
        }

        if (dateEl && !dateEl.querySelector("input")) {
            const value = oldDate && oldDate !== "ДД.ММ.ГГГГ" ? convertRuDateToInputDate(oldDate) : "";
            dateEl.innerHTML = `<input class="task-date-input" type="date" value="${value}">`;
        }

        if (userEl && !userEl.querySelector("input")) {
            const value = oldUser && oldUser !== "Ответственный" ? oldUser : "";
            userEl.innerHTML = `<input class="task-user-input" type="text" placeholder="Ответственный" value="${value}">`;
        }

        if (removeEl) {
            removeEl.innerText = "✕";
            removeEl.style.cursor = "pointer";
            removeEl.addEventListener("click", () => row.remove());
        }

        const inputs = row.querySelectorAll("input");
        inputs.forEach(input => {
            input.addEventListener("input", () => updateTaskRowState(row));
        });

        updateTaskRowState(row);
    });
}

function convertRuDateToInputDate(date) {
    const match = date.match(/^(\d{2})\.(\d{2})\.(\d{4})$/);
    if (!match) return "";
    const [, day, month, year] = match;
    return `${year}-${month}-${day}`;
}

function convertInputDateToRuDate(date) {
    if (!date) return null;
    const [year, month, day] = date.split("-");
    return `${day}.${month}.${year}`;
}

function createEmptyTaskRow() {
    const row = document.createElement("div");
    row.className = "task-row";

    row.innerHTML = `
        <div class="task-name"><input class="task-name-input" type="text" placeholder="Задача"></div>
        <div class="task-date"><input class="task-date-input" type="date"></div>
        <div class="task-user"><input class="task-user-input" type="text" placeholder="Ответственный"></div>
        <div class="task-remove">✕</div>
    `;

    return row;
}

function addTaskRow() {
    const addTaskBtn = document.getElementById("addTaskBtn");
    const newRow = createEmptyTaskRow();
    addTaskBtn.insertAdjacentElement("beforebegin", newRow);
    normalizeExistingTaskRows();
}

function showThinkingStatus() {
    let block = document.getElementById("thinkingBlock");

    if (!block) {
        block = document.createElement("div");
        block.id = "thinkingBlock";
        block.className = "thinking-block";

        block.innerHTML = `
            <div class="thinking-left">
                <div class="thinking-title">SekretaR работает</div>
                <div class="thinking-text">Анализирую встречу, выделяю смысл и задачи...</div>
            </div>

            <div class="neural-flow">
                <svg class="neural-svg" viewBox="0 0 180 64">
                    <path class="neural-path" d="M10 32 C45 5, 75 5, 90 32 S135 59, 170 32" />
                    <path class="neural-path" d="M10 18 C50 45, 80 45, 100 18 S140 -5, 170 18" />
                    <path class="neural-path" d="M10 46 C45 20, 75 20, 95 46 S135 72, 170 46" />

                    <path class="neural-trail trail-one" d="M10 32 C45 5, 75 5, 90 32 S135 59, 170 32" />
                    <path class="neural-trail trail-two" d="M10 18 C50 45, 80 45, 100 18 S140 -5, 170 18" />
                    <path class="neural-trail trail-three" d="M10 46 C45 20, 75 20, 95 46 S135 72, 170 46" />
                </svg>
            </div>
        `;

        const blocks = document.querySelectorAll(".block");
        if (blocks[1]) {
            blocks[1].insertAdjacentElement("afterend", block);
        }
    }
}

function hideThinkingStatus() {
    const status = document.getElementById("thinkingBlock");
    if (status) status.remove();
}

function renderResult(data) {
    window.currentMeetingData = data;
    const blocks = document.querySelectorAll(".block-text");

    if (blocks[0]) blocks[0].innerText = data.transcript || "Нет данных";
    if (blocks[1]) blocks[1].innerText = data.summary || "Нет summary";

    const addTaskBtn = document.getElementById("addTaskBtn");
    document.querySelectorAll(".task-row").forEach(el => el.remove());

    (data.tasks || []).forEach(task => {
        const row = createEmptyTaskRow();
        row.querySelector(".task-name-input").value = task.text || "";
        row.querySelector(".task-user-input").value = task.assignee || "";
        addTaskBtn.insertAdjacentElement("beforebegin", row);
    });

    normalizeExistingTaskRows();
}

async function uploadAudio(file) {
    showThinkingStatus();

    const formData = new FormData();
    const filename = file.name || "recording.webm";

    formData.append("file", file, filename);
    formData.append("user_id", getUserId());
    formData.append("meeting_id", "meeting_" + Date.now());

    try {
        const response = await fetch("/upload", {
            method: "POST",
            headers: getAuthHeaders(),
            body: formData
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error("HTTP " + response.status + ": " + text);
        }

        const result = await response.json();

        renderResult(result);
        hideThinkingStatus();

    } catch (error) {
        hideThinkingStatus();
        alert("Ошибка загрузки: " + (error?.message || error));
    }
}

document.addEventListener("DOMContentLoaded", () => {

    normalizeExistingTaskRows();

    const addTaskBtn = document.getElementById("addTaskBtn");

    if (addTaskBtn) {
        addTaskBtn.addEventListener("click", () => {
            addTaskRow();
        });
    }

    const params = new URLSearchParams(window.location.search);
    const returnedMeetingId = params.get("meeting_id");

    if (returnedMeetingId) {
        showThinkingStatus();

        fetch(`/meeting/${returnedMeetingId}`, {
            method: "GET",
            headers: getAuthHeaders()
        })
            .then(res => res.json())
            .then(data => {
                hideThinkingStatus();

                if (data && !data.error) {
                    renderResult({
                        transcript: data.transcript || "",
                        summary: data.summary || "",
                        tasks: data.tasks || []
                    });
                } else {
                    alert("Результат встречи пока не найден");
                }
            })
            .catch(() => {
                hideThinkingStatus();
                alert("Не удалось загрузить результат встречи");
            });
    }

    const uploadBtn = document.getElementById("uploadBtn");
    const recordBtn = document.getElementById("recordBtn");

    const modal = document.getElementById("recordModal");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const uploadAltBtn = document.getElementById("uploadAltBtn");
    const browserRecordBtn = document.getElementById("browserRecordBtn");
    const openRecorderBtn = document.getElementById("openRecorderBtn");
    const installRecorderBtn = document.getElementById("installRecorderBtn");

    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    if (browserRecordBtn) {
        browserRecordBtn.addEventListener("click", async () => {

            if (!isRecording) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    mediaRecorder.ondataavailable = (event) => {
                        audioChunks.push(event.data);
                    };

                    mediaRecorder.onstop = () => {
                        const blob = new Blob(audioChunks, { type: "audio/webm" });

                        const file = new File([blob], "recording.webm", {
                            type: "audio/webm"
                        });

                        uploadAudio(file);
                    };

                    mediaRecorder.start();
                    isRecording = true;

                    browserRecordBtn.innerText = "⏹ Остановить запись";

                } catch (err) {
                    alert("Не удалось получить доступ к микрофону");
                }

            } else {
                mediaRecorder.stop();
                isRecording = false;

                browserRecordBtn.innerText = "🌐 Записать в браузере";

                if (modal) {
                    modal.style.display = "none";
                }
            }

        });
    }

    if (openRecorderBtn) {
        openRecorderBtn.addEventListener("click", () => {
            const userId = getUserId();
            const deviceId = getDeviceId();
            const meetingId = "meeting_" + Date.now();

            const returnUrl = new URL(window.location.href);
            returnUrl.searchParams.set("meeting_id", meetingId);
            returnUrl.searchParams.set("user_id", userId);

            window.location.href =
                `sekretar://record?meeting_id=${encodeURIComponent(meetingId)}` +
                `&user_id=${encodeURIComponent(userId)}` +
                `&device_id=${encodeURIComponent(deviceId)}` +
                `&return_url=${encodeURIComponent(returnUrl.toString())}`;
        });
    }

    if (installRecorderBtn) {
        installRecorderBtn.addEventListener("click", () => {
            window.location.href = "/downloads/sekretar-recorder-beta.apk";
        });
    }

    const input = document.createElement("input");
    input.type = "file";
    input.accept = "audio/*,video/*";
    input.style.display = "none";
    document.body.appendChild(input);

    if (uploadBtn) {
        uploadBtn.addEventListener("click", () => input.click());
    }

    input.addEventListener("change", () => {
        const file = input.files[0];
        if (file) uploadAudio(file);
    });

    if (recordBtn) {
        recordBtn.addEventListener("click", () => {
            modal.style.display = "flex";
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }

    if (uploadAltBtn) {
        uploadAltBtn.addEventListener("click", () => {
            modal.style.display = "none";
            input.click();
        });
    }

    async function downloadDocx(type) {
        const blocks = document.querySelectorAll(".block-text");

        const transcript = blocks[0]?.innerText?.trim() || "";
        const summary = blocks[1]?.innerText?.trim() || "";

        const userId = getUserId();

        let payload = {
            title: "SekretaR",
            transcript: "",
            summary: "",
            user_id: userId
        };

        if (type === "transcript") {
            payload.title = "Транскрипция встречи";
            payload.transcript = transcript;
        }

        if (type === "summary") {
            payload.title = "Краткое содержание встречи";
            payload.summary = summary;
        }

        const response = await fetch("/export_docx", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders()
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            alert("Не удалось скачать Word-документ");
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = type === "transcript"
            ? "sekretar_transcript.docx"
            : "sekretar_summary.docx";

        document.body.appendChild(a);
        a.click();
        a.remove();

        window.URL.revokeObjectURL(url);
    }

    const downloadTranscriptDocx = document.getElementById("downloadTranscriptDocx");
    const downloadSummaryDocx = document.getElementById("downloadSummaryDocx");

    if (downloadTranscriptDocx) {
        downloadTranscriptDocx.addEventListener("click", () => {
            downloadDocx("transcript");
        });
    }

    if (downloadSummaryDocx) {
        downloadSummaryDocx.addEventListener("click", () => {
            downloadDocx("summary");
        });
    }

    const confirmBtn = document.getElementById("confirmBtn");

    if (confirmBtn) {
        confirmBtn.addEventListener("click", async () => {
            const meetingData = window.currentMeetingData;

            if (!meetingData || !meetingData.meeting_id) {
                alert("Нет активной встречи для отправки задач");
                return;
            }

            const taskRows = document.querySelectorAll(".task-row");

            const tasks = Array.from(taskRows).map(row => {
                const text = row.querySelector(".task-name-input")?.value?.trim() || "";
                const dueDate = row.querySelector(".task-date-input")?.value?.trim() || "";
                const assignee = row.querySelector(".task-user-input")?.value?.trim() || "";

                return {
                    text,
                    due_date: dueDate,
                    assignee
                };
            }).filter(task => task.text && task.due_date);

            if (tasks.length === 0) {
                alert("Нет заполненных задач с датой");
                return;
            }

            confirmBtn.disabled = true;
            confirmBtn.innerText = "Добавляю в календарь...";

            try {
                const response = await fetch("/confirm_tasks", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        ...getAuthHeaders()
                    },
                    body: JSON.stringify({
                        meeting_id: meetingData.meeting_id,
                        summary: meetingData.summary || "",
                        tasks
                    })
                });

                const result = await response.json();

                if (result.calendar_link) {
                    alert("Задачи добавлены в календарь");
                    window.open(result.calendar_link, "_blank");
                } else {
                    alert("Календарь не вернул ссылку");
                    console.log("confirm_tasks result:", result);
                }

            } catch (e) {
                console.error(e);
                alert("Ошибка отправки задач в календарь");
            } finally {
                confirmBtn.disabled = false;
                confirmBtn.innerText = "Подтвердить задачи";
            }
        });
    }

});