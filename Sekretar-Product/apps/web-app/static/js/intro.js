function startApp() {
    const overlay = document.getElementById('intro-overlay');
    const video = document.getElementById('intro-video');
    const logo = document.querySelector('.logo-wrapper');

    logo.style.display = 'none';
    overlay.style.display = 'flex';

    video.currentTime = 0;

    video.onended = () => {
        window.location.href = "/static/app.html";
    };

    video.play().catch(() => {
        window.location.href = "/static/app.html";
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("start-btn");
    if (btn) btn.onclick = startApp;
});