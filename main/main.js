//처음 화면에서 로그인 화면으로 전환
document.addEventListener("click", function () {
  const page1 = document.getElementById("page1");
  const page2 = document.getElementById("page2");

  page1.classList.add("hidden");

  setTimeout(function () {
    page1.style.display = "none";
    page2.style.display = "flex";
    page2.classList.remove("hidden");
  }, 500); // css transition 시간이랑 맞추기
});

// 로그인 form
let loginFrom = document.querySelector(".my-form");

loginFrom.addEventListener("submit", (e) => {
  e.preventDefault();
  let email = document.getElementById("email");
  let password = document.getElementById("password");

  console.log("Email: ", email.value);
  console.log("Password: ", password.value);

  //이후에 API로 전송하는 부분이 필요함
});
