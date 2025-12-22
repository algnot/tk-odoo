console.log("✅ survey_certificate.js loaded");

const interval = setInterval(() => {
    const container =
        document.querySelector('.o_survey_results') ||
        document.querySelector('.o_survey_finished') ||
        document.querySelector('.o_survey_container');

    if (!container) return;

    if (document.getElementById('survey-certificate-btn')) {
        clearInterval(interval);
        return;
    }

    const parts = window.location.pathname.split('/');
    const token = parts[parts.length - 1];

    if (!token || token.length < 10) {
        console.log("❌ token not found in URL");
        return;
    }

    const btn = document.createElement("a");
    btn.id = "survey-certificate-btn";
    btn.href = `/survey/certificate/${token}`;
    btn.textContent = "🎓 View Certificate";
    btn.className = "btn btn-primary btn-lg mt-3";

    container.appendChild(btn);

    console.log("✅ Certificate button injected");
    clearInterval(interval);

}, 400);
