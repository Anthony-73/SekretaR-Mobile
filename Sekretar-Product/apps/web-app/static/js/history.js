document.addEventListener("DOMContentLoaded", () => {
    const protocolTab = document.getElementById("protocolTab");
    const historyTab = document.getElementById("historyTab");
    const protocolContent = document.getElementById("protocolContent");
    const historyContent = document.getElementById("historyContent");

    if (!protocolTab || !historyTab || !protocolContent || !historyContent) {
        return;
    }

    async function loadHistory() {
        const userId = localStorage.getItem("user_id");

        if (!userId) {
            historyContent.innerHTML = "";
            return;
        }

        try {
            const res = await fetch(`/history/${userId}`, {
                headers: {
                    "device-id": localStorage.getItem("device_id")
                }
            });
            const data = await res.json();

            if (!Array.isArray(data) || data.length === 0) {
                historyContent.innerHTML = "";
                return;
            }

            historyContent.innerHTML = `
                <div style="max-height:420px; overflow-y:auto; padding-right:8px;">
                    ${data.map(item => {
                        const summary = item.summary
                            ? item.summary.slice(0, 120)
                            : "Без краткого содержания";

                        const date = item.created_at
                            ? new Date(item.created_at).toLocaleString("ru-RU")
                            : "";

                        return `
                            <div class="task-row" data-meeting-id="${item.id}" style="cursor:pointer; border-color:rgba(212,175,55,0.25);">
                                <div class="task-name">${summary}${item.summary && item.summary.length > 120 ? "..." : ""}</div>
                                <div class="task-date">${date}</div>
                                <div class="task-user">Открыть</div>
                                <div class="task-remove">›</div>
                            </div>
                        `;
                    }).join("")}
                </div>
            `;

            historyContent.querySelectorAll(".task-row").forEach(row => {
                row.addEventListener("click", async () => {
                    const meetingId = row.dataset.meetingId;
                    await openHistoryMeeting(meetingId);
                });
            });

        } catch (e) {
            console.error("History load error:", e);
            historyContent.innerHTML = "";
        }
    }

    async function openHistoryMeeting(meetingId) {
        if (typeof showThinkingStatus === "function") {
            showThinkingStatus();
        }

        try {
            const res = await fetch(`/meeting/${meetingId}`, {
                headers: {
                    "device-id": localStorage.getItem("device_id"),
                    "user-id": localStorage.getItem("user_id")
                }
            });
            const data = await res.json();

            if (typeof hideThinkingStatus === "function") {
                hideThinkingStatus();
            }

            if (!data || data.error) {
                alert("Встреча не найдена");
                return;
            }

            if (typeof renderResult === "function") {
                renderResult({
                    meeting_id: meetingId,
                    transcript: data.transcript || "",
                    summary: data.summary || "",
                    tasks: data.tasks || []
                });
            }

            protocolContent.style.display = "none";
            historyContent.style.display = "none";

        } catch (e) {
            if (typeof hideThinkingStatus === "function") {
                hideThinkingStatus();
            }

            console.error("Meeting load error:", e);
            alert("Ошибка загрузки встречи");
        }
    }

    async function checkNewMeetings() {
        const userId = typeof getUserId === "function"
            ? getUserId()
            : localStorage.getItem("user_id");

        const deviceId = typeof getDeviceId === "function"
            ? getDeviceId()
            : localStorage.getItem("device_id");

        if (!userId || !deviceId) return;

        try {
            const res = await fetch(`/meetings/new/${userId}`, {
                headers: {
                    "device-id": deviceId
                }
            });

            const data = await res.json();

            if (!Array.isArray(data) || data.length === 0) {
                const existingModal = document.getElementById("newMeetingsModal");
                if (existingModal) existingModal.remove();
                return;
            }

            showNewMeetingsModal(data);

        } catch (e) {
            console.error("New meetings load error:", e);
        }
    }

    function showNewMeetingsModal(meetings) {
        const oldModal = document.getElementById("newMeetingsModal");
        if (oldModal) oldModal.remove();

        const modal = document.createElement("div");
        modal.id = "newMeetingsModal";

        modal.style.cssText = `
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.78);
            z-index: 1200;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 18px;
            box-sizing: border-box;
        `;

        modal.innerHTML = `
            <div style="
                width: 460px;
                max-width: 100%;
                max-height: 80vh;
                overflow-y: auto;
                background: #0c0c0c;
                border: 1px solid rgba(212,175,55,0.35);
                border-radius: 16px;
                padding: 22px;
                box-shadow: 0 0 40px rgba(0,0,0,0.6);
                color: #e8d8a3;
                font-family: Georgia, serif;
            ">
                <div style="font-size:20px; margin-bottom:8px;">
                    🔔 Новые обработанные встречи
                </div>

                <div style="font-size:14px; opacity:0.65; margin-bottom:18px;">
                    У вас ${meetings.length} ${getMeetingWord(meetings.length)}. Нажмите на встречу, чтобы открыть её.
                </div>

                <div id="newMeetingsList"></div>

                <button id="closeNewMeetingsModal" class="main-btn" style="margin-top:16px; opacity:0.65;">
                    Позже
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        const list = modal.querySelector("#newMeetingsList");

        meetings.forEach(item => {
            const row = document.createElement("div");
            row.className = "task-row";
            row.style.cursor = "pointer";
            row.style.borderColor = "rgba(212,175,55,0.35)";

            const summary = item.summary
                ? item.summary.slice(0, 90)
                : "Встреча без краткого содержания";

            const date = item.created_at
                ? new Date(item.created_at).toLocaleString("ru-RU")
                : "";

            row.innerHTML = `
                <div class="task-name">${summary}${item.summary && item.summary.length > 90 ? "..." : ""}</div>
                <div class="task-date">${date}</div>
                <div class="task-user">Открыть</div>
                <div class="task-remove">›</div>
            `;

            row.addEventListener("click", async () => {
                await openHistoryMeeting(item.id);
                modal.remove();
                await checkNewMeetings();
            });

            list.appendChild(row);
        });

        const closeBtn = modal.querySelector("#closeNewMeetingsModal");
        closeBtn.addEventListener("click", () => {
            modal.remove();
        });
    }

    function getMeetingWord(count) {
        if (count % 10 === 1 && count % 100 !== 11) return "новая встреча";
        if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) return "новые встречи";
        return "новых встреч";
    }

    protocolTab.addEventListener("click", () => {
        protocolContent.style.display = "none";
        historyContent.style.display = "none";
    });

    historyTab.addEventListener("click", () => {
        protocolContent.style.display = "none";
        historyContent.style.display = "block";
        loadHistory();
    });

    checkNewMeetings();

    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) {
            checkNewMeetings();
        }

    });

    window.addEventListener("focus", () => {
        checkNewMeetings();
    });

    setInterval(() => {
        checkNewMeetings();
    }, 30000);

});