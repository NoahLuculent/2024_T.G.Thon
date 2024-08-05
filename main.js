document.addEventListener("click", function () {
  const page1 = document.getElementById("page1");
  const page2 = document.getElementById("page2");

  // Fade out current page
  page1.classList.add("hidden");

  // After fade-out complete, fade-in new page
  setTimeout(function () {
    page1.style.display = "none";
    page2.style.display = "flex";
    page2.classList.remove("hidden");
  }, 500); // Matches the CSS transition duration
});
