document.addEventListener("DOMContentLoaded", function () {
  // Toggle the nav menu visibility on click
  document.getElementById("mobile-menu").addEventListener("click", function () {
    const navMenuContainer = document.querySelector(".nav-menu-container");
    navMenuContainer.style.display =
      navMenuContainer.style.display === "block" ? "none" : "block";
  });
});