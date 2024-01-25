document.addEventListener("DOMContentLoaded", function () {
  const menuButton = document.getElementById("mobile-menu");
  const navMenuContainer = document.querySelector(".nav-menu-container");
  menuButton.addEventListener("click", function () {
    // Toggle the nav menu visibility
    const isMenuVisible = navMenuContainer.style.display === "block";
    navMenuContainer.style.display = isMenuVisible ? "none" : "block";
    // Toggle the button's visibility
    menuButton.style.display = isMenuVisible ? "block" : "none";
  });
});
