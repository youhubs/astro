document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    const flashMessages = document.querySelector(".flash-messages");
    if (flashMessages) {
      flashMessages.classList.add("hide");
    }
  }, 3000);
});
