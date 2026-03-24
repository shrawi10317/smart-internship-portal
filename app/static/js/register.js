document.addEventListener("DOMContentLoaded", function () {

    const togglePassword = document.querySelector(".toggle-password");
    const toggleConfirm = document.querySelector(".toggle-password-confirm");

    const password = document.getElementById("password");
    const confirm = document.getElementById("confirmPassword");

    togglePassword.addEventListener("click", function () {
        password.type = password.type === "password" ? "text" : "password";
    });

    toggleConfirm.addEventListener("click", function () {
        confirm.type = confirm.type === "password" ? "text" : "password";
    });

});