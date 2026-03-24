let timeLeft = 30;
const timerText = document.getElementById("timer");
const resendBtn = document.getElementById("resendBtn");

const countdown = setInterval(() => {

    timeLeft--;

    if (timeLeft > 0) {
        timerText.innerText = "Resend OTP in " + timeLeft + "s";
    } else {
        clearInterval(countdown);
        timerText.innerText = "";
        resendBtn.classList.remove("disabled");
    }

}, 1000);