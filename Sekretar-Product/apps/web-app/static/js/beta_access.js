(function () {
    function getOrCreateDeviceId() {
        let deviceId = localStorage.getItem("device_id");

        if (!deviceId) {
            deviceId = crypto.randomUUID();
            localStorage.setItem("device_id", deviceId);
        }

        return deviceId;
    }

    function getOrCreateUserId() {
        let userId = localStorage.getItem("user_id");

        if (!userId) {
            userId = crypto.randomUUID();
            localStorage.setItem("user_id", userId);
        }

        return userId;
    }

    window.SekretaRAuth = {
        getDeviceId: getOrCreateDeviceId,
        getUserId: getOrCreateUserId,
        getHeaders: function () {
            return {
                "device-id": getOrCreateDeviceId(),
                "user-id": getOrCreateUserId()
            };
        }
    };
})();

document.addEventListener("DOMContentLoaded", async () => {
    const appContainer = document.querySelector(".container");

    if (!appContainer) return;

    const deviceId = window.SekretaRAuth.getDeviceId();
    const userId = window.SekretaRAuth.getUserId();

    async function checkAccess() {
        localStorage.removeItem("beta_access_code");

        const sessionCode = sessionStorage.getItem("beta_access_code");

        if (sessionCode === "SVEN") {
            return true;
        }

        const res = await fetch("/beta/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...window.SekretaRAuth.getHeaders()
            },
            body: JSON.stringify({
                device_id: deviceId,
                user_id: userId
            })
        });

        const data = await res.json();
        return data.status === "ok";
    }

    function showAccessScreen() {
        appContainer.innerHTML = `
            <div class="logo">SekretaR</div>
            <div class="logo-line"></div>

            <div class="block" style="max-width:520px; margin:40px auto;">
                <div class="block-title">Закрытый бета-доступ</div>

                <div class="block-text" style="margin-bottom:18px; line-height:1.5;">
                    SekretaR работает в режиме закрытого тестирования.<br><br>

                    Рабочее окно сервиса: с 09:00 до 18:00.<br>
                    В остальное время сайт может находиться в разработке.<br><br>

                    ⚠️ Запись через iPhone (iOS) временно не поддерживается.<br>
                    ⚠️ Аудиофайлы из облака (Google Drive и др.) могут не загружаться — сначала скачайте файл на устройство.
                </div>

                <input
                    id="betaCodeInput"
                    type="text"
                    placeholder="Введите код доступа"
                    style="
                        width:100%;
                        box-sizing:border-box;
                        padding:14px;
                        border-radius:12px;
                        border:1px solid rgba(212,175,55,0.35);
                        background:rgba(232,216,163,0.08);
                        color:#e8d8a3;
                        font-family:Georgia,serif;
                        font-size:16px;
                        outline:none;
                    "
                >

                <button class="main-btn" id="betaAccessBtn" type="button">
                    Войти
                </button>

                <div id="betaAccessMessage" style="
                    margin-top:14px;
                    font-size:14px;
                    opacity:0.75;
                "></div>
            </div>
        `;

        const input = document.getElementById("betaCodeInput");
        const button = document.getElementById("betaAccessBtn");
        const message = document.getElementById("betaAccessMessage");

        async function activate() {
            const code = input.value.trim();

            if (!code) {
                message.innerText = "Введите код доступа.";
                return;
            }

            button.disabled = true;
            button.innerText = "Проверяю код...";

            try {
                const res = await fetch("/beta/activate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        ...window.SekretaRAuth.getHeaders()
                    },
                    body: JSON.stringify({
                        code,
                        device_id: deviceId,
                        user_id: userId
                    })
                });

                const data = await res.json();

                if (data.status === "ok") {
                    if (code === "SVEN") {
                        sessionStorage.setItem("beta_access_code", "SVEN");
                    } else {
                        localStorage.setItem("beta_access_granted", "true");
                        localStorage.setItem("beta_access_code", code);
                    }

                    window.location.reload();
                    return;
                }

                message.innerText = data.message || "Доступ не разрешён.";

            } catch (e) {
                message.innerText = "Ошибка проверки доступа.";
            } finally {
                button.disabled = false;
                button.innerText = "Войти";
            }
        }

        button.addEventListener("click", activate);

        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") activate();
        });
    }

    try {
        const hasAccess = await checkAccess();

        if (!hasAccess) {
            showAccessScreen();
        }

    } catch (e) {
        showAccessScreen();
    }
});